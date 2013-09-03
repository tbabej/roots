from django.conf.urls import patterns, url
from events.views import EventListView

urlpatterns = patterns('',
    url(r'^$', EventListView.as_view(), name="events_event_list")
)
