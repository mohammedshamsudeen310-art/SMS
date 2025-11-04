# from django.db import models
# from django.utils import timezone
# from accounts.models import CustomUser, Student
# from academics.models import Subject, ClassRoom, Session


# # ===============================
# # 🔹 ATTENDANCE SESSION
# # ===============================
# class AttendanceSession(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
#     session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
#     teacher = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         limit_choices_to={'role': 'teacher'}
#     )
#     date = models.DateField(default=timezone.now)
#     start_time = models.TimeField(default=timezone.now)
#     end_time = models.TimeField(blank=True, null=True)

#     class Meta:
#         ordering = ['-date']

#     def __str__(self):
#         return f"{self.subject.name} - {self.date}"


# # ===============================
# # 🔹 ATTENDANCE RECORD
# # ===============================
# class AttendanceRecord(models.Model):
#     session = models.ForeignKey(
#         AttendanceSession,
#         on_delete=models.CASCADE,
#         related_name="records"
#     )
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     status = models.CharField(
#         max_length=10,
#         choices=[('Present', 'Present'), ('Absent', 'Absent')]
#     )
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("session", "student")
#         ordering = ['student__user__first_name']

#     def __str__(self):
#         return f"{self.student} - {self.status}"


# # ===============================
# # 🔹 ATTENDANCE SUMMARY (optional but useful)
# # ===============================
# class AttendanceSummary(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_summary')
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     total_classes = models.PositiveIntegerField(default=0)
#     attended_classes = models.PositiveIntegerField(default=0)

#     class Meta:
#         unique_together = ("student", "subject")

#     def attendance_percentage(self):
#         if self.total_classes == 0:
#             return 0
#         return round((self.attended_classes / self.total_classes) * 100, 2)

#     def __str__(self):
#         return f"{self.student} - {self.subject} ({self.attendance_percentage()}%)"
