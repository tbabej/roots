from django.views.generic.list import ListView

from .models import Leaflet


class LeafletListView(ListView):

    model = Leaflet
    context_object_name = 'leaflets'
