from django import forms
from .models import Payment, StudentFeeRecord,FeeType, BulkFeeAssignment, Invoice
from academics.models import Session


class PaymentForm(forms.ModelForm):
    """
    Form for recording payments towards a student's fee record.
    """
    class Meta:
        model = Payment
        fields = [
            "student_fee",
            "amount",
            "payment_method",
            "date_paid",
        ]

        widgets = {
            "student_fee": forms.Select(attrs={
                "class": "form-control",
            }),
            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
                "placeholder": "Enter amount paid",
            }),
            "payment_method": forms.Select(attrs={
                "class": "form-control",
            }),
            "reference": forms.HiddenInput(), # Reference will be auto-generated
            "date_paid": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
        }

        labels = {
            "student_fee": "Student Fee Record",
            "amount": "Amount Paid (₵)",
            "payment_method": "Payment Method",
            "reference": "Payment Reference",
            "date_paid": "Date Paid",
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean_reference(self):
        reference = self.cleaned_data.get("reference")
        if Payment.objects.filter(reference=reference).exists():
            raise forms.ValidationError("This reference already exists.")
        return reference
    
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['student_fee'].queryset = StudentFeeRecord.objects.filter(is_cleared=False)





class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ["name", "description", "amount", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter fee name", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BulkFeeForm(forms.ModelForm):
    class Meta:
        model = BulkFeeAssignment
        fields = ["fee_type", "session", "term", "total_amount", "target_class"]
        widgets = {
            "fee_type": forms.Select(attrs={"class": "form-control"}),
            "session": forms.Select(attrs={"class": "form-control"}),
            "term": forms.Select(attrs={"class": "form-control"}),
            "total_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "target_class": forms.Select(attrs={"class": "form-control"}),
        }


class StudentFeeForm(forms.ModelForm):
    class Meta:
        model = StudentFeeRecord
        fields = ["student", "fee_type", "session", "term", "total_amount", "amount_paid"]
        widgets = {
            "student": forms.Select(attrs={"class": "form-control"}),
            "fee_type": forms.Select(attrs={"class": "form-control"}),
            "session": forms.Select(attrs={"class": "form-control"}),
            "term": forms.Select(attrs={"class": "form-control"}),
            "total_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "amount_paid": forms.NumberInput(attrs={"class": "form-control"}),
        }




class BulkFeeCreationForm(forms.Form):
    session = forms.ModelChoiceField(queryset=Session.objects.all())
    term = forms.ChoiceField(choices=[
        ("1st", "1st Term"),
        ("2nd", "2nd Term"),
        ("3rd", "3rd Term"),
    ])
    fee_type = forms.ModelChoiceField(queryset=FeeType.objects.all())
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2)


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['student', 'session', 'term', 'total_due', 'total_paid', 'is_paid']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'session': forms.TextInput(attrs={'class': 'form-control'}),
            'term': forms.TextInput(attrs={'class': 'form-control'}),
            'total_due': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_paid': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
