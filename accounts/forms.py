from django import forms
from .models import (
    CustomUser,
    Admin,
    Teacher,
    Student,
    Parent,
    Accountant,
)

# ============================================================
# 🔹 1️⃣ Base Profile Form (Shared Fields)
# ============================================================
class BaseProfileForm(forms.ModelForm):
    class Meta:
        # All models inheriting BaseProfile have these fields
        fields = ["date_of_birth", "gender", "address", "photo"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


# ============================================================
# 🔹 2️⃣ Role-Specific Profile Forms
# ============================================================
class AdminProfileForm(BaseProfileForm):
    class Meta(BaseProfileForm.Meta):
        model = Admin
        fields = BaseProfileForm.Meta.fields + ["designation"]
        widgets = {
            **BaseProfileForm.Meta.widgets,
            "designation": forms.TextInput(attrs={"class": "form-control"}),
        }


class TeacherProfileForm(BaseProfileForm):
    class Meta(BaseProfileForm.Meta):
        model = Teacher
        fields = BaseProfileForm.Meta.fields + [
            "staff_id",
            "qualification",
            "department",
            "hire_date",
        ]
        widgets = {
            **BaseProfileForm.Meta.widgets,
            "staff_id": forms.TextInput(attrs={"class": "form-control"}),
            "qualification": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "hire_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class AccountantProfileForm(BaseProfileForm):
    class Meta(BaseProfileForm.Meta):
        model = Accountant
        fields = BaseProfileForm.Meta.fields + ["employee_id", "hire_date"]
        widgets = {
            **BaseProfileForm.Meta.widgets,
            "employee_id": forms.TextInput(attrs={"class": "form-control"}),
            "hire_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


from django import forms
from .models import Parent, Student
from django.contrib.auth.models import User  # ✅ To handle username/email linkage
class ParentProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        }),
        label="Username"
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        }),
        label="Email Address"
    )
    fullname = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name'
        }),
        label="Full Name"
    )

    children = forms.ModelMultipleChoiceField(
        queryset=Student.objects.select_related('user').all().order_by('user__first_name'),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'multi-select',
            'data-placeholder': 'Search and select children...'
        }),
        label="Children (Students)"
    )

    class Meta:
        model = Parent
        fields = [
            'username',
            'email',
            'fullname',
            'gender',
            'address',
            'photo',
            'occupation',
            'relationship',
            'children',
        ]
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Enter home address'
            }),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Parent occupation'
            }),
            'relationship': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 💥 Totally remove the date_of_birth field (fixes your issue)
        self.fields.pop("date_of_birth", None)

        self.fields['children'].label_from_instance = (
            lambda obj: f"{obj.user.get_full_name()} ({obj.student_id})"
            if obj.user else f"{obj.student_id}"
        )


# ============================================================
# 🔹 3️⃣ Student Form (Note: Student is NOT a BaseProfile)
# ============================================================
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "admission_date",
            "date_of_birth",
            "current_class",
            "section",
            "guardian_name",
            "guardian_contact",
            "is_active",
        ]
        widgets = {
            "student_id": forms.HiddenInput(), # Auto-generated, hide from form
            "admission_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "current_class": forms.Select(attrs={"class": "form-control"}),
            "section": forms.TextInput(attrs={"class": "form-control"}),
            "guardian_name": forms.TextInput(attrs={"class": "form-control"}),
            "guardian_contact": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, you can set initial values or modify fields here
        self.fields['email'].required = False


# ============================================================
# 🔹 4️⃣ User Account Info Form (Shared)
# ============================================================
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email", "phone_number", "role"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.HiddenInput(),  # 👈 hide it from the form
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:  # Only check uniqueness if email is provided
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this email already exists.")
        return email




from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import BaseProfile  # adjust based on your actual profile model

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = BaseProfile
        fields = ['photo', 'gender', 'date_of_birth', 'address']  # add others if needed

class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter current password'})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )



