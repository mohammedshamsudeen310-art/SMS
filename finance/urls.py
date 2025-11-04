from django.urls import path
from . import views

urlpatterns = [
    path("invoices/", views.manage_invoices, name="manage_invoices"),
    path('invoice/<int:pk>/edit/', views.edit_invoice, name='edit_invoice'),
    path('invoice/<int:pk>/delete/', views.delete_invoice, name='delete_invoice'),


    path("record-payment/", views.record_payment, name="record_payment"),
    path("summary-json/", views.finance_summary_json, name="finance_summary_json"),

    path("invoices/json/", views.invoices_json, name="invoices_json"),
    path("invoice/<int:invoice_id>/download/", views.download_invoice_pdf, name="download_invoice_pdf"),

    path("financial-report/", views.financial_report, name="financial_report"),
    path("financial-report/export-excel/", views.export_financial_report_excel, name="export_financial_report_excel"),
    path("financial-report/export-pdf/", views.export_financial_report_pdf, name="export_financial_report_pdf"),
    path('my-fees/', views.student_fees, name='student_fees'),
    path("financial/invoices/", views.my_invoices, name="my_invoices"),
    path("parent/payment-history/", views.parent_payment_history, name="parent_payment_history"),

    path("parent/payment-history/export/excel/", views.export_payment_history_excel, name="export_payment_history_excel"),
    path("parent/payment-history/export/pdf/", views.export_payment_history_pdf, name="export_payment_history_pdf"),

    path("fees/", views.manage_fees, name="manage_fees"),
    path("fees/types/", views.fee_types, name="fee_types"),
    path('edit/<int:pk>/', views.edit_fee_type, name='edit_fee_type'),
    path('delete/<int:pk>/', views.delete_fee_type, name='delete_fee_type'),
    path("fees/add/", views.add_fee, name="add_fee"),

    path("bulk-create-fee-records/", views.bulk_create_fee_records, name="bulk_create_fee_records"),
    path("fees/bulk/", views.bulk_fee_assignment, name="bulk_fee_assignment"),

    path('ajax/student-search/', views.student_search, name='student_search'),

]
