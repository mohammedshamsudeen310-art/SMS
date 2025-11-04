from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.utils.crypto import get_random_string
from .models import Payment, Invoice, StudentFeeRecord, FinanceSummary,BulkFeeAssignment
from academics.models import Session, ClassRoom
from accounts.models import CustomUser, Student, Teacher


# ======================================================
# 🔹 Centralized Finance Summary Updater
# ======================================================
def update_finance_summary():
    """Recalculate and update FinanceSummary totals."""
    summary, _ = FinanceSummary.objects.get_or_create(id=1)

    # ====== Users and Invoices ======
    summary.total_students = CustomUser.objects.filter(role="student").count()
    summary.total_teachers = CustomUser.objects.filter(role="teacher").count()
    summary.total_invoices = Invoice.objects.count()

    # ====== Fees and Payments ======
    total_paid = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
    total_due = Invoice.objects.aggregate(total=Sum("total_due"))["total"] or 0
    total_unpaid = Invoice.objects.filter(is_paid=False).aggregate(total=Sum("balance"))["total"] or 0

    # ====== Calculate pending balance ======
    summary.total_fees_paid = total_paid
    summary.total_fees_pending = max(total_due - total_paid, 0)
    summary.total_fees_unpaid = total_unpaid

    summary.save()


# ======================================================
# 🔹 Auto-update summary when key models change
# ======================================================
@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
@receiver(post_save, sender=Invoice)
@receiver(post_delete, sender=Invoice)
@receiver(post_save, sender=StudentFeeRecord)
@receiver(post_delete, sender=StudentFeeRecord)
def update_finance_summary_on_change(sender, instance, **kwargs):
    """Trigger summary recalculation on relevant model changes."""
    update_finance_summary()


# ======================================================
# 🔹 Sync Invoice when a Payment is made
# ======================================================
@receiver(post_save, sender=Payment)
def update_invoice_on_payment(sender, instance, created, **kwargs):
    """Whenever a new payment is made, update the linked invoice totals."""
    if created and hasattr(instance, "invoice") and instance.invoice:
        invoice = instance.invoice
        invoice.total_paid = (invoice.total_paid or 0) + (instance.amount or 0)
        invoice.balance = max(invoice.total_due - invoice.total_paid, 0)
        invoice.is_paid = invoice.balance <= 0
        invoice.save()


# ======================================================
# 🔹 Auto-create or update Invoice from StudentFeeRecord
# ======================================================
@receiver(post_save, sender=StudentFeeRecord)
def update_or_create_invoice(sender, instance, **kwargs):
    """
    Automatically create or update invoice when student fee record is saved.
    Ensures invoice reflects cumulative total_due, total_paid, and balance.
    """
    invoice, created = Invoice.objects.get_or_create(
        student=instance.student,
        session=instance.session,
        term=instance.term,
        defaults={
            "invoice_number": f"INV-{get_random_string(8).upper()}",
            "total_due": 0,
            "total_paid": 0,
            "balance": 0,
        },
    )

    # 🔹 Recalculate all fee records for that student/session/term
    records = StudentFeeRecord.objects.filter(
        student=instance.student,
        session=instance.session,
        term=instance.term,
    )

    total_due = sum(record.total_amount for record in records)
    total_paid = sum(record.amount_paid for record in records)
    balance = total_due - total_paid

    invoice.total_due = total_due
    invoice.total_paid = total_paid
    invoice.balance = balance
    invoice.is_paid = balance <= 0
    invoice.save()



# ======================================================
# 🔹 Auto-create StudentFeeRecord when BulkFeeAssignment is created
# ======================================================

from django.db import IntegrityError

@receiver(post_save, sender=BulkFeeAssignment)
def create_fee_records_for_students(sender, instance, created, **kwargs):
    if created:
        if instance.target_class:
            students = Student.objects.filter(current_class=instance.target_class)
        else:
            students = Student.objects.all()

        for student in students:
            try:
                # Only create if not already existing for this student/session/term/fee_type
                StudentFeeRecord.objects.get_or_create(
                    student=student,
                    fee_type=instance.fee_type,
                    session=instance.session,
                    term=instance.term,
                    defaults={
                        "total_amount": instance.total_amount,
                        "amount_paid": 0,
                    },
                )
            except IntegrityError:
                # In case of a rare race condition, just skip gracefully
                continue
