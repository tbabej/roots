from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.utils.translation import ugettext_lazy as _

from django.views.generic import TemplateView
from django.views.generic.detail import DetailView


from base.util import class_view_decorator

from schools.forms import AddressForm
from .forms import UserProfileBasicForm, UserProfileEventForm, UsernameForm

from .models import UserProfile


@class_view_decorator(login_required)
class UserProfileUpdate(TemplateView):

    template_name = 'profiles/userprofile_form.html'

    basic_profile_form = None
    event_profile_form = None
    address_form = None
    name_form = None

    @property
    def forms(self):
        return (
            self.basic_profile_form,
            self.event_profile_form,
            self.address_form,
            self.name_form
        )

    def set_forms(self):
        if all(form is not None for form in self.forms):
            return

        if self.request.POST:
            self.basic_profile_form = UserProfileBasicForm(self.request.POST,
                                   instance=self.request.user.userprofile)
            self.event_profile_form = UserProfileEventForm(self.request.POST,
                                   instance=self.request.user.userprofile)
            self.address_form = AddressForm(self.request.POST,
                               instance=self.request.user.userprofile.address)
            self.name_form = UsernameForm(self.request.POST,
                               instance=self.request.user)
        else:
            self.basic_profile_form = UserProfileBasicForm(
                               instance=self.request.user.userprofile)
            self.event_profile_form = UserProfileEventForm(
                               instance=self.request.user.userprofile)
            self.address_form = AddressForm(
                               instance=self.request.user.userprofile.address)
            self.name_form = UsernameForm(instance=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)

        self.set_forms()

        context_forms = {
            'basic_profile_form': self.basic_profile_form,
            'event_profile_form': self.event_profile_form,
            'address_form': self.address_form,
            'name_form': self.name_form,
            }

        context.update(context_forms)

        return context

    def post(self, request, *args, **kwargs):
        self.set_forms()

        forms_valid = all(form.is_valid() for form in self.forms)

        if forms_valid:
            self.name_form.save()
            self.event_profile_form.save()
            address = self.address_form.save()
            profile = self.basic_profile_form.save(commit=False)
            profile.address = address
            profile.save()

        if any(form.has_changed() for form in self.forms):
            if forms_valid:
                messages.success(request, _("Profile successfully updated."))
        else:
            messages.info(request, _("Nothing has changed."))

        return self.get(request)


class UserProfileDetail(DetailView):

    model = UserProfile
    context_object_name = 'profile'

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))

        return user.userprofile
