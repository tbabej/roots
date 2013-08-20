from django.conf.urls import patterns, url

from profiles.views import UserProfileUpdate

urlpatterns = patterns('',
    url(r'update$', UserProfileUpdate.as_view(),
        name='profiles_userprofile_update'),
)