from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from base.util import class_view_decorator
from base.views import RedirectBackView

from .models import Event, EventUserRegistration


class EventListView(ListView):

    model = Event
    context_object_name = 'events'


class EventDetailView(DetailView):

    model = Event
    context_object_name = 'event'


@class_view_decorator(login_required)
class EventUserRegisterView(RedirectBackView):

    default_return_view = 'events_event_list'

    def dispatch(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs['event_id'])

        # Check if user is not already registered
        registrations = EventUserRegistration.objects.filter(
            user=request.user,
            event=event).count()

        if registrations:
            message = _('You are already registered to the %s') % event
            messages.add_message(request, messages.ERROR, message)
            return super(EventUserRegisterView, self).dispatch(request,
                                                               *args,
                                                               **kwargs)

        if event.registration_open():
            registration = EventUserRegistration(user=request.user, event=event)
            registration.save()

            message = _('Successfully registered to the %s') % event
            messages.add_message(request, messages.INFO, message)
        else:
            message = _('Registration to the %s is not open.') % event
            messages.add_message(request, messages.ERROR, message)

        return super(EventUserRegisterView, self).dispatch(request,
                                                           *args, **kwargs)
