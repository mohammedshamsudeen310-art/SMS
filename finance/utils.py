from django.db.models import Sum, Count
from accounts.models import Student, Teacher
from .models import Invoice, FinanceSummary

def update_finance_summary():
    """
    Refreshes the FinanceSummary totals based on current financial data.
    """
    summary, _ = FinanceSummary.objects.get_or_create(id=1)

    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_invoices = Invoice.objects.count()

    # Aggregate payment data
    total_paid = Invoice.objects.aggregate(total=Sum("total_paid"))["total"] or 0
    total_due = Invoice.objects.aggregate(total=Sum("total_due"))["total"] or 0
    total_balance = Invoice.objects.aggregate(total=Sum("balance"))["total"] or 0

    # Split between paid/pending/unpaid
    fully_paid = Invoice.objects.filter(is_paid=True).count()
    partially_paid = Invoice.objects.filter(is_paid=False, total_paid__gt=0).count()
    unpaid = Invoice.objects.filter(total_paid=0).count()

    # Update the summary table
    summary.total_students = total_students
    summary.total_teachers = total_teachers
    summary.total_invoices = total_invoices
    summary.total_fees_paid = total_paid
    summary.total_fees_pending = total_balance  # pending = total balance left
    summary.total_fees_unpaid = total_due - total_paid
    summary.save()
