from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div

from .models import Competition, Season


class CompetitionRegistrationForm(forms.Form):

    competition = forms.ModelChoiceField(queryset=Competition.objects.all())

    def __init__(self, *args, **kwargs):
        super(CompetitionRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_exampleForm'
        self.helper.form_class = 'blueForms form-horizontal'
        self.helper.form_mehthod = 'post'
        self.helper.form_action = ''
        self.helper.label_class = 'col-lg-6'
        self.helper.field_class = 'col-lg-2'
        self.helper.layout = Layout(
            Div(
                Div('competition', css_class='col-lg-12'),
                Div(Submit('submit', 'Submit', css_class='center-block'),
                    css_class="col-lg-12"),
                css_class='center-block'
            )
        )


class SeasonJoinForm(forms.Form):

    # season = forms.ModelChoiceField(queryset=SeasonJoinForm.user.competitions
    #                                         .filter(is_active=True))
    season = forms.ModelChoiceField(queryset=Season.objects.all())
