from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic import ListView

from problems.models import UserSolution
from problems.forms import UserSolutionForm

from .forms import CompetitionRegistrationForm
from .models import Competition, CompetitionUserRegistration, Season


class CompetitionRegistrationView(FormView):

    form_class = CompetitionRegistrationForm
    template_name = 'competitions/competition_registration.html'
    success_url = 'registration/successful/'

    def form_valid(self, form):
        registration = CompetitionUserRegistration()
        registration.competition = form.cleaned_data['competition']
        registration.user = self.request.user.userprofile
        registration.save()
        return super(CompetitionRegistrationView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *arg, **kwarg):
        return super(CompetitionRegistrationView, self).dispatch(*arg, **kwarg)


class CompetitionDiscussionView(DetailView):
    model = Competition
    context_object_name = 'competition'
    template_name = 'competitions/competition_discussion.html'

    def get_object(self):
        competition = get_object_or_404(
            Competition,
            pk=self.kwargs.get('competition_id')
        )

        return competition


class SeasonResultsView(DetailView):
    model = Season
    context_object_name = 'season'
    template_name = 'competitions/season_results.html'

    def get_context_data(self, **kwargs):
        context = super(SeasonResultsView, self).get_context_data(**kwargs)

        # Generate a list of seasons for this competition
        competition = self.object.competition
        seasons = Season.objects.filter(competition=competition).order_by('-start')
        context['competition_seasons'] = seasons

        return context

class SeasonDetailView(DetailView):
    model = Season
    context_object_name = 'season'

    def get_context_data(self, *args, **kwargs):
        context = super(SeasonDetailView, self).get_context_data(*args,
                                                                 **kwargs)
        # Generate a list of seasons for this competition
        competition = self.object.competition
        seasons = Season.objects.filter(competition=competition).order_by('-start')
        context['competition_seasons'] = seasons

        # Find UserSolution objects for the problems
        context['solutions'] = dict()

        for series in self.object.series_set.all():

            context['solutions'][series.pk] = dict()

            for problem in series.problemset.problems.all():
                solutions = UserSolution.objects.filter(
                                                 user=self.request.user.pk,
                                                 problem=problem.pk)
                solution = solutions[0] if solutions else None

                context['solutions'][series.pk][problem.pk] = solution

        # Construct form objects
        context['forms'] = dict()

        for series in self.object.series_set.all():

            context['forms'][series.pk] = dict()

            for problem in series.problemset.problems.all():
                solutions = UserSolution.objects.filter(
                                                 user=self.request.user.pk,
                                                 problem=problem.pk)
                if not solutions:
                    form = UserSolutionForm(initial={'problem': problem.pk,
                                                     'series': series.pk})
                else:
                    form = UserSolutionForm(
                               initial={'problem': problem.pk,
                                        'series': series.pk,
                                        'solution': solutions[0].solution})

                context['forms'][series.pk][problem.pk] = form

        return context


class LatestSeasonDetailView(SeasonDetailView):
    def get_object(self):
        competition = get_object_or_404(Competition, pk=self.kwargs.get('competition_id'))
        return competition.season_set.order_by('-end')[0]


class LatestSeasonResultsView(SeasonResultsView):
    def get_object(self):
        competition = get_object_or_404(Competition, pk=self.kwargs.get('competition_id'))
        return competition.season_set.order_by('-end')[0]
