from django.conf.urls import patterns, url
from functools import partial

from problems.models import UserSolution

from .views import download_protected_file

urlpatterns = patterns('',
    url(r'solutions/(?P<path>.*)$', download_protected_file,
        dict(path_prefix='solutions/', model_class=UserSolution),
        name='download_solution'),
)
