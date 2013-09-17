from django.conf.urls import patterns, url

from .views import UserProfileUpdate

urlpatterns = patterns('',
    url(r'update$', UserProfileUpdate.as_view(),
        name='profiles_userprofile_update'),
)