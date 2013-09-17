from django import forms

from .models import Competition


class CompetitionRegistrationForm(forms.Form):

    competition = forms.ModelChoiceField(queryset=Competition.objects.all())