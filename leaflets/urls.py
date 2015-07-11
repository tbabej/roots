from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from .views import (LeafletListView, LeafletCompetitionListView,
                    LastLeafletView)

urlpatterns = patterns('',
    url(r'^$', LeafletListView.as_view(), name="leaflets_leaflet_list"),
    url(_(r'^competitions/(?P<competition_id>\d+)/$'),
        LeafletCompetitionListView.as_view(),
        name="leaflets_leaflet_competition_list"),
    url(_(r'^competitions/(?P<competition_id>\d+)/last/$'),
        LastLeafletView.as_view(),
        name="leaflets_leaflet_competition_last"),
    )
