from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import (EventListView, EventUserRegisterView,
                    EventDetailView)

urlpatterns = patterns('',
    url(
        r'^$',
        EventListView.as_view(),
        name="events_event_list"
    ),
    url(
        r'^(?P<pk>\d+)/$',
        EventDetailView.as_view(),
        name="events_event_detail"
    ),
    url(
        _(r'^register/(?P<event_id>\d+)/user/$'),
        EventUserRegisterView.as_view(),
        name="events_event_user_registration"
    ),
    url(
        _(r'^register/(?P<event_id>\d+)/organizer/$'),
        EventUserRegisterView.as_view(),
        name="events_event_org_registration"
    ),
)
