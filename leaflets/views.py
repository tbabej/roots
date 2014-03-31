from django.views.generic.list import ListView

from .models import Leaflet
from  competitions.models import Competition
from django.shortcuts import get_object_or_404


class LeafletViewContextItem:
    def __init__(self, competition=None, leaflets=None):
        self.competition = competition
        self.leaflets = leaflets

class LeafletListView(ListView):

    model = Leaflet    
    context_object_name = 'competitions'   
    template_name = "leaflets/leaflet_list.html"
    
    def get_context_data(self, **kwargs):
        """Return the last 2 published leaflets in each competition"""
        context = super(ListView, self).get_context_data(**kwargs)
        d=[]
        
        for c in Competition.objects.all() :
            item = LeafletViewContextItem()
            item.competition = c
            item.leaflets = Leaflet.objects.\
                filter(competition = c).\
                order_by('-year').order_by('-issue')[:2]
            d.append(item)
        context['data']=d     
        return context
        
class LeafletCompetitionListView(ListView):
    
    model = Leaflet
    contex_object_name = 'leaflets'
    template_name ="leaflets/leaflet_competition_list.html"
    
    def get_context_data(self, **kwargs):
        """Return all leaflets in given competition"""
        context = super(ListView, self).get_context_data(**kwargs)
        c = get_object_or_404(Competition,id = self.kwargs['competition_id'])
        item = LeafletViewContextItem()
        item.competition = c
        item.leaflets = Leaflet.objects.\
            filter(competition = c).\
            order_by('-year').order_by('-issue')
        context['data']=item   
        return context             
