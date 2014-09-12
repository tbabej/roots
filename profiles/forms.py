from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

from crispy_forms.helper import FormHelper

from django.contrib.auth.models import User

from .models import UserProfile


class UsernameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsernameForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = UserProfile
        exclude = ('user', 'address')
        help_texts = {
            'school': string_concat(
                    _('Pick the school from the list. '
                      'If your school is not available, please, '),
                    '<a href="',
                    reverse_lazy('schools_school_create'),
                    _('">add it.</a>')
                ),
            'phone_number': _('Needed to contact you in case you qualified '
                              'to attend a camp.'),
            'school_class': _('Name of your class in the school, such '
                              'as "4.A".'),
            'parent_phone_number': _("Mobile phone number of the parent, or "
                                     "of any other lawful representative.")
        }

EVENT_ONLY_FIELDS = ('date_of_birth', 'parent_phone_number', 'sex')


class UserProfileBasicForm(UserProfileForm):
    """
    Form containing the fields considered necessary for user participating
    in the competition.
    """

    class Meta(UserProfileForm.Meta):
            exclude = (UserProfileForm.Meta.exclude +
                       EVENT_ONLY_FIELDS)


class UserProfileEventForm(UserProfileForm):
    """
    Form containing the fields considered necessary for user attending
    camps.
    """

    class Meta(UserProfileForm.Meta):
            fields = EVENT_ONLY_FIELDS
