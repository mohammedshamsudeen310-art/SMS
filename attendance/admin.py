from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "classroom", "date")
    list_filter = ("subject", "classroom", "date")
    search_fields = ("subject__name", "classroom__name")
    ordering = ("-date",)


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "student", "status")
    list_filter = ("status", "session__subject", "session__classroom")
    search_fields = ("student__first_name", "student__last_name", "session__subject__name")
