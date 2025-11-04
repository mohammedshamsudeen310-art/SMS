from django.contrib import admin
from .models import ResultRecord, ResultSummary

@admin.register(ResultRecord)
class ResultRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "term", "session", "total_score", "grade", "teacher")
    list_filter = ("session", "term", "classroom")
    search_fields = ("student__user__username", "subject__name")

admin.site.register(ResultSummary)
