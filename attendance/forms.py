from django import forms
from .models import AttendanceSession, AttendanceRecord
from academics.models import ClassRoom, Subject
from accounts.models import Student

# ============================================================
# 1️⃣ Attendance Session Form
# ============================================================
class AttendanceSessionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True
    )

    class Meta:
        model = AttendanceSession
        fields = ["subject", "classroom", "date"]

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop("teacher", None)  # Teacher profile
        super().__init__(*args, **kwargs)

        if teacher:
            # Filter subjects assigned to this teacher
            self.fields["subject"].queryset = Subject.objects.filter(teacher=teacher.user)

            # Filter classrooms where this teacher has subjects
            self.fields["classroom"].queryset = ClassRoom.objects.filter(
                subjects__teacher=teacher.user
            ).distinct()

            # Pre-select if only one option
            if self.fields["subject"].queryset.count() == 1:
                self.fields["subject"].initial = self.fields["subject"].queryset.first()

            if self.fields["classroom"].queryset.count() == 1:
                self.fields["classroom"].initial = self.fields["classroom"].queryset.first()


# ============================================================
# 2️⃣ Attendance Record Form
# ============================================================
class AttendanceRecordForm(forms.Form):
    """
    Dynamically builds fields for each student in the classroom.
    """
    STATUS_CHOICES = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("excused", "Excused"),
    ]

    def __init__(self, *args, **kwargs):
        session = kwargs.pop("session", None)
        super().__init__(*args, **kwargs)

        if not session:
            return

        # Get all students in the session's classroom
        students = Student.objects.filter(current_class=session.classroom, is_active=True)

        # Dynamically create a field for each student
        for student in students:

            # ▶️ STATUS FIELD
            self.fields[f"status_{student.id}"] = forms.ChoiceField(
                choices=self.STATUS_CHOICES,
                widget=forms.Select(attrs={"class": "form-select"}),
                label=student.user.get_full_name() or student.user.username
            )

