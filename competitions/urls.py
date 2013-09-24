from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import CompetitionRegistrationView, SeasonJoinView

urlpatterns = patterns('',
    url(r'^$', CompetitionRegistrationView.as_view(),
        name='competitions_competition_register'),
    url(r'^registration/successful/', TemplateView.as_view(
        template_name='competitions/competition_registration_successful.html'),
        name='competitions_competition_register_success'),
    url(r'^join/$', SeasonJoinView.as_view(),
        name='competitions_season_join'),
)