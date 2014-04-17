from django import forms

from .models import UserSolution


class UserSolutionForm(forms.ModelForm):
    class Meta:
        model = UserSolution
        fields = ['solution', 'problem']
        widgets = {
            'problem': forms.HiddenInput
        }
