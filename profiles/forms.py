from django.forms import ModelForm
from profiles.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'competes')
