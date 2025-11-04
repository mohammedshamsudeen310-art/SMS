from django import forms
from .models import ResultRecord


class ResultEntryForm(forms.ModelForm):
    class Meta:
        model = ResultRecord
        fields = ['test_score', 'exam_score']
        widgets = {
            'test_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '40'}),
            'exam_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '60'}),
        }
