# Create your views here.

from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from base.util import class_view_decorator

from profiles.forms import UserProfileForm
from profiles.models import UserProfile

from django.contrib import messages


@class_view_decorator(login_required)
class UserProfileUpdate(UpdateView):

    form_class = UserProfileForm
    success_url = '/profiles/update'

    def get_object(self):
        return UserProfile.objects.all().filter(user=self.request.user)[0]

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Hello world.')
        return super(UserProfileUpdate, self).form_valid(form)
