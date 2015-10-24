from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic import ListView

from problems.models import UserSolution
from problems.forms import UserSolutionForm

from .forms import CompetitionRegistrationForm
from .models import Competition, CompetitionUserRegistration, Season, Series

from avatar.models import Avatar

class CurrentSiteCompetitionMixin(object):
    """
    Little mixin which gives access to the relevant competition
    for the view.
    """

    @property
    def competition(self):
        try:
            competition_id = self.kwargs.get('competition_id')
            return Competition.objects.get(pk=competition_id)
        except Competition.DoesNotExist:
            return Competition.get_by_current_site()


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


class CompetitionDiscussionView(CurrentSiteCompetitionMixin, DetailView):
    model = Competition
    context_object_name = 'competition'
    template_name = 'competitions/competition_discussion.html'

    def get_object(self):
        return self.competition


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

        competitors_ids = list(self.object.competitors.values_list('pk', flat=True))
        context['user_avatars_list'] = list(Avatar.objects.filter(
            user__pk__in=competitors_ids,
            primary=True).values_list('user__pk', flat=True))

        return context

class SeriesResultExportTeXView(DetailView):
    model = Series
    context_object_name = 'series'
    template_name = 'competitions/series_result.tex'

    def get_context_data(self, **kwargs):
        context = super(SeriesResultExportTeXView,
                        self).get_context_data(**kwargs)

        # Generate a list of problems in this series
        problems = self.object.problemset.problems.values_list('pk', flat=True)
        counts = {}
        histograms = {}

        for problem_pk in problems:
            # Construct a histogram for each user
            histograms[problem_pk] = []

            # Count the total number of solutions of the problem
            solutions = UserSolution.objects.filter(problem=problem_pk)
            counts[problem_pk] = solutions.count()

            for score in range(10):
                # Filter out solutions that have this score
                solutions_with_score = solutions.filter(score=score).count()
                histograms[problem_pk].append(solutions_with_score)


        context['problems'] = problems
        context['problems_count'] = counts
        context['problems_histogram'] = histograms

        return context

class SeasonResultExportTeXView(DetailView):
    model = Season
    context_object_name = 'season'
    template_name = 'competitions/season_result.tex'


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

            # If there is no problemset assigned, skip
            if not series.problemset:
                continue

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

            # If there is no problemset assigned, skip
            if not series.problemset:
                continue

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


class LatestSeasonDetailView(CurrentSiteCompetitionMixin, SeasonDetailView):
    def get_object(self):
        return self.competition.season_set.order_by('-end')[0]


class LatestSeasonResultsView(CurrentSiteCompetitionMixin, SeasonResultsView):
    def get_object(self):
        return self.competition.season_set.order_by('-end')[0]
