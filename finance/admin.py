from django.contrib import admin
from .models import FeeType, StudentFeeRecord, Payment, Invoice, FinanceSummary, Session, BulkFeeAssignment


# ===========================
# 🔹 Fee Type Admin
# ===========================
@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


# ===========================
# 🔹 Student Fee Record Admin
# ===========================
@admin.register(StudentFeeRecord)
class StudentFeeRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "fee_type", "term", "session", "total_amount", "amount_paid", "balance", "is_cleared")
    list_filter = ("term", "session", "is_cleared")
    search_fields = ("student__user__username", "fee_type__name")
    autocomplete_fields = ("student", "fee_type", "session")
    readonly_fields = ("balance", "is_cleared")
    date_hierarchy = "date_created"


# ===========================
# 🔹 Payment Admin
# ===========================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("reference", "student_fee", "amount", "payment_method", "date_paid", "received_by")
    list_filter = ("payment_method", "date_paid")
    search_fields = ("reference", "student_fee__student__user__username")
    autocomplete_fields = ("student_fee", "received_by")
    date_hierarchy = "date_paid"


# ===========================
# 🔹 Invoice Admin
# ===========================
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "student", "session", "term", "total_due", "total_paid", "balance", "is_paid")
    list_filter = ("term", "session", "is_paid")
    search_fields = ("invoice_number", "student__user__username")
    autocomplete_fields = ("student", "session")
    readonly_fields = ("balance", "is_paid")
    date_hierarchy = "date_issued"


# ===========================
# 🔹 Finance Summary Admin
# ===========================
@admin.register(FinanceSummary)
class FinanceSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "total_students", "total_teachers", "total_invoices",
        "total_fees_paid", "total_fees_pending", "total_fees_unpaid", "last_updated"
    )
    readonly_fields = (
        "total_students", "total_teachers", "total_invoices",
        "total_fees_paid", "total_fees_pending", "total_fees_unpaid", "last_updated"
    )

    def has_add_permission(self, request):
        # Limit to only one Finance Summary record
        if FinanceSummary.objects.exists():
            return False
        return True


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name",)
    list_filter = ("is_current",)


@admin.register(BulkFeeAssignment)
class BulkFeeAssignmentAdmin(admin.ModelAdmin):
    list_display = ("fee_type", "target_class", "term", "total_amount", "session", "date_created")
    list_filter = ("term", "session", "target_class")
    search_fields = ("fee_type__name",)
