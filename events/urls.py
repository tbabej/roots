from django.conf.urls import patterns, url

from .views import EventListView, EventUserRegisterView

urlpatterns = patterns('',
    url(
        r'^$',
        EventListView.as_view(),
        name="events_event_list"
    ),
    url(
        r'register/(?P<event_id>\d+)/user/$',
        EventUserRegisterView.as_view(),
        name="events_event_user_registration"
    ),
    url(
        r'register/(?P<event_id>\d+)/organizer/$',
        EventUserRegisterView.as_view(),
        name="events_event_org_registration"
    ),
)
