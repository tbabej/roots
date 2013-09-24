from django import forms

from .models import Competition, Season


class CompetitionRegistrationForm(forms.Form):

    competition = forms.ModelChoiceField(queryset=Competition.objects.all())


class SeasonJoinForm(forms.Form):

    #season = forms.ModelChoiceField(queryset=SeasonJoinForm.user.competitions
    #                                         .filter(is_active=True))
    season = forms.ModelChoiceField(queryset=Season.objects.all())
