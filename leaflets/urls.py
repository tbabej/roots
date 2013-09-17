from django.conf.urls import patterns, url

from .views import LeafletListView

urlpatterns = patterns('',
    url(r'^$', LeafletListView.as_view(), name="leaflets_leaflet_list")
)
