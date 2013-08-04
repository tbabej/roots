from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from problems.models import Problem


class ProblemListView(ListView):

    model = Problem
    context_object_name = 'problems'


class ProblemDetailView(DetailView):

    model = Problem
    context_object_name = 'problem'
