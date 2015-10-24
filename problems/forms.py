from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from base.forms import MultiFileField
from competitions.models import Series


class UserSolutionForm(forms.Form):
    solution = MultiFileField(min_num=1,
                              max_size=settings.ROOTS_MAX_SOLUTION_SIZE,
                              max_total_size=settings.ROOTS_MAX_SOLUTION_SIZE)
    problem = forms.IntegerField(widget=forms.HiddenInput)
    series = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        """
        Since series is a part of the POST request, check that problem
        belongs to this series and that this series is not past its deadline.
        """

        series = Series.objects.get(pk=self.cleaned_data['series'])

        if series.is_past_submission_deadline():
            raise forms.ValidationError(_("Series is past its submission deadline"))

        if not series.problemset.problems.filter(pk=self.cleaned_data['problem']).exists():
            raise forms.ValidationError(_("Problem does not belong to the series"))



class ImportCorrectedSolutionsForm(forms.Form):
    zipfile = forms.FileField()
    # TODO: include field for people that corrected the solutions
