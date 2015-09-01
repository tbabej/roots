from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from .views import (CompetitionDiscussionView, CompetitionRegistrationView,
                    SeasonDetailView, SeasonResultsView, LatestSeasonDetailView,
                    LatestSeasonResultsView, SeriesResultExportTeXView,
                    SeasonResultExportTeXView)

urlpatterns = patterns('',
    url(r'^$', CompetitionRegistrationView.as_view(),
        name='competitions_competition_register'),
    url(_(r'^registration/successful/'), TemplateView.as_view(
        template_name='competitions/competition_registration_successful.html'),
        name='competitions_competition_register_success'),
    url(_(r'^season/(?P<pk>\d+)$'), SeasonDetailView.as_view(),
        name='competitions_season_detail'),
    url(_(r'^season/latest/(?P<competition_id>\d+)?$'),
        LatestSeasonDetailView.as_view(),
        name='competitions_season_detail_latest'),
    url(_(r'^season/results/latest/(?P<competition_id>\d+)?$'),
        LatestSeasonResultsView.as_view(),
        name='competitions_season_results_latest'),
    url(_(r'^season/results/(?P<pk>\d+)$'), SeasonResultsView.as_view(),
        name='competitions_season_results'),
    url(_(r'^series/results/tex/(?P<pk>\d+)$'),
        SeriesResultExportTeXView.as_view(),
        name='competitions_series_results_tex'),
    url(_(r'^season/results/tex/(?P<pk>\d+)$'),
        SeasonResultExportTeXView.as_view(),
        name='competitions_season_results_tex'),
    url(_(r'^discussion/(?P<competition_id>\d+)?'),
        CompetitionDiscussionView.as_view(),
        name='competitions_competition_discussion'),
)
