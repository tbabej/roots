from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import SchoolCreateView


urlpatterns = patterns('',
    url(_(r'^create$'), SchoolCreateView.as_view(),
        name='schools_school_create'),
)
