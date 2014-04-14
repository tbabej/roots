from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from competitions.models import Competition

from .models import Leaflet


class LeafletViewContextItem(object):
    def __init__(self, competition=None, leaflets=None):
        self.competition = competition
        self.leaflets = leaflets


class LeafletCompetitionViewContextItem(object):
    def __init__(self, year=None, leaflets=None):
        self.year = year
        self.leaflets = leaflets


class LeafletListView(ListView):

    model = Leaflet
    context_object_name = 'competitions'
    template_name = "leaflets/leaflet_list.html"

    def get_context_data(self, **kwargs):
        """Return the last 2 published leaflets in each competition"""
        context = super(ListView, self).get_context_data(**kwargs)
        data = []
        competitions = Competition.objects.all()
        for competition in competitions:
            item = LeafletViewContextItem()
            item.competition = competition
            item.leaflets = Leaflet.objects.\
                                    filter(competition=competition).\
                                    order_by('-year', '-issue')[:5]
            data.append(item)
        context['data'] = data
        return context


class LeafletCompetitionListView(ListView):

    model = Leaflet
    contex_object_name = 'leaflets'
    template_name = "leaflets/leaflet_competition_list.html"

    def get_context_data(self, **kwargs):
        """Return all leaflets in given competition grouped by years"""
        context = super(ListView, self).get_context_data(**kwargs)
        data = []

        competition = get_object_or_404(Competition,
                                        id=self.kwargs['competition_id'])
        leaflets = Leaflet.objects\
                           .filter(competition=competition)\
                           .order_by('-year', 'issue')
        previous_leaflet = leaflets[0]

        item = LeafletCompetitionViewContextItem(
            year=previous_leaflet.year,
            leaflets=[])

        item.year = previous_leaflet.year
        for leaflet in leaflets:

            if leaflet.year != previous_leaflet.year:
                data.append(item)
                item = LeafletCompetitionViewContextItem(
                           year=leaflet.year,
                           leaflets=[])

            item.leaflets.append(leaflet)
            previous_leaflet = leaflet

        data.append(item)
        context['data'] = data
        context['competition'] = competition

        return context
