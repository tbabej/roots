from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import UserProfileUpdate

urlpatterns = patterns('',
    url(_(r'update$'), UserProfileUpdate.as_view(),
        name='profiles_userprofile_update'),
)