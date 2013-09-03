from django.views.generic.list import ListView
from events.models import Event


class EventListView(ListView):

    model = Event
    context_object_name = 'events'
