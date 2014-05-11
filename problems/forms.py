from django import forms
from django.conf import settings

from base.forms import MultiFileField


class UserSolutionForm(forms.Form):
    solution = MultiFileField(min_num=1,
                              max_size=settings.ROOTS_MAX_SOLUTION_SIZE,
                              max_total_size=settings.ROOTS_MAX_SOLUTION_SIZE)
    problem = forms.IntegerField(widget=forms.HiddenInput)


class ImportCorrectedSolutionsForm(forms.Form):
    zipfile = forms.FileField()
    # TODO: include field for people that corrected the solutions
