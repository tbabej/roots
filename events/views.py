from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from base.util import class_view_decorator
from base.views import RedirectBackView

from .models import Event, EventUserRegistration


class EventListView(ListView):

    model = Event
    context_object_name = 'events'


@class_view_decorator(login_required)
class EventUserRegisterView(RedirectBackView):

    default_return_view = 'events_event_list'

    def dispatch(self, request, *args, **kwargs):
        event = Event.objects.get(pk=kwargs['event_id'])

        if event.registration_open():
            registration = EventUserRegistration(user=request.user, event=event)
            registration.save()

            message = 'Successfully registered to the %s' % event
            messages.add_message(request, messages.INFO, message)
        else:
            message = 'Registration to the %s is not open.' % event
            messages.add_message(request, messages.ERROR, message)

        return super(EventUserRegisterView, self).dispatch(request,
                                                           *args, **kwargs)




