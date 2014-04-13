from django.conf.urls import patterns, url

from .views import LeafletListView, LeafletCompetitionListView

urlpatterns = patterns('',
    url(r'^$', LeafletListView.as_view(), name="leaflets_leaflet_list"),
    url(r'^competitions/(?P<competition_id>\d+)/$',
    LeafletCompetitionListView.as_view(),
    name="leaflets_leaflet_competition_list"),
    )
