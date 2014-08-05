from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView


from base.util import class_view_decorator

from .forms import UserProfileForm
from .models import UserProfile


@class_view_decorator(login_required)
class UserProfileUpdate(UpdateView):

    form_class = UserProfileForm
    success_url = '/profiles/update'

    def get_object(self):
        return UserProfile.objects.all().filter(user=self.request.user)[0]

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO, 'Hello world.')
        return super(UserProfileUpdate, self).form_valid(form)


class UserProfileDetail(DetailView):

    model = UserProfile
    context_object_name = 'profile'

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        return user.userprofile
