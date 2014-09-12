from django import forms
from crispy_forms.helper import FormHelper

from .models import School, Address


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = Address


class SchoolForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = School
        exclude = ('address',)
