from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from problems.models import UserSolution

from .views import download_protected_file

urlpatterns = patterns('',
    url(_(r'solutions/(?P<path>.*)$'), download_protected_file,
        dict(path_prefix='solutions/', model_class=UserSolution),
        name='download_solution'),
)
