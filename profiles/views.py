# Create your views here.

from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from base.util import class_view_decorator

from profiles.forms import UserProfileForm
from profiles.models import UserProfile


@class_view_decorator(login_required)
class UserProfileUpdate(UpdateView):

    form_class = UserProfileForm
    success_url = '/profiles/update'

    def get_object(self):
        return UserProfile.objects.all().filter(user=self.request.user)[0]
