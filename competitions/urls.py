from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from .views import (CompetitionRegistrationView, SeasonDetailView,
                    SeasonResultsView)

urlpatterns = patterns('',
    url(r'^$', CompetitionRegistrationView.as_view(),
        name='competitions_competition_register'),
    url(_(r'^registration/successful/'), TemplateView.as_view(
        template_name='competitions/competition_registration_successful.html'),
        name='competitions_competition_register_success'),
    url(_(r'^season/(?P<pk>\d+)$'), SeasonDetailView.as_view(),
        name='competitions_season_detail'),
    url(_(r'^season/results/(?P<pk>\d+)$'), SeasonResultsView.as_view(),
        name='competitions_season_results'),
)
