from django.contrib import admin
from .models import ClassRoom, Subject, Enrollment

admin.site.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "capacity")
    list_filter = ("section",)
    search_fields = ("name", "section")
    ordering = ("name",)




@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'classroom', 'teacher')
    list_filter = ('classroom', 'teacher')
    search_fields = ('name', 'code')
    ordering = ('classroom', 'name')



@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "date_enrolled")
    list_filter = ("subject", "date_enrolled")
    search_fields = ("student__user__username", "student__user__first_name", "student__user__last_name", "subject__name")
