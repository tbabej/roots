from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import get_model
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from base.util import (with_timestamp, with_author, remove_accents,
                       YearSegment, simple_solution_sum, simple_series_solution_sum)


# Competition-related models
@with_author
@with_timestamp
class Competition(models.Model):
    """
    Represents a competition. One roots site will usually hold several
    competitions, as there are usually several age categories or several
    subjects categories. Or both.
    """

    name = models.CharField(max_length=100,
                            verbose_name=_('competition name'),
                            unique=True)
    organizer_group = models.ForeignKey(Group,
                                        blank=True,
                                        null=True,
                                        verbose_name=_('organizer group'))

    # Fields added via foreign keys:

    #  competitionorgregistration_set
    #  competitionuserregistration_set
    #  gallery_set
    #  leaflet_set
    #  post_set
    #  problemset_set
    #  season_set
    #  user_set

    def __unicode__(self):
        return self.name

    @cached_property
    def active_season(self):
        season_candidates = self.season_set.filter(start__lt=now(),
                                                   end__gt=now())
        if season_candidates.exists():
            return season_candidates[0]
        else:
            return None

    def get_all_user_seasons(self, user):
        """
        Yields the all the seasons the user competed in.
        """

        for season in self.season_set.all():
            if season.competitors.filter(pk=user.pk).exists():
                yield season

    def get_best_user_ranking(self, user):
        """
        Returns the best ranking of this user and the season in which
        it occured.

        Returns (None, None) if no user ranking found (user would have to never
        submit a solution).
        """

        best_rank = None
        best_season = None

        for season in self.get_all_user_seasons(user):
            rank = season.get_user_ranking(user)
            if best_rank < rank:
                best_rank = rank
                best_season = season

        return best_rank, best_season

    class Meta:
        ordering = ['name']
        verbose_name = _('competition')
        verbose_name_plural = _('competitions')


@with_author
@with_timestamp
class CompetitionUserRegistration(models.Model):
    """
    Represents a relation between user and competition. User himself can
    register into competition if he satisfies the conditions.
    """

    competition = models.ForeignKey('competitions.Competition',
                                    verbose_name=_('competition'))
    user = models.ForeignKey('auth.User',
                             verbose_name=_('user'))

    def __unicode__(self):
        return (self.user.__unicode__() + unicode(_(" competes in ")) +
                self.competition.__unicode__())

    class Meta:
        ordering = ['added_at']
        verbose_name = _('user registration')
        verbose_name_plural = _('user registrations')


@with_author
@with_timestamp
class CompetitionOrgRegistration(models.Model):
    """
    Represents a relation between organizer and competition. Organizer can
    help organize multiple competitions. Organizer registrations have to
    be approved.
    """

    competition = models.ForeignKey('competitions.Competition',
                                    verbose_name=_('competition'))
    organizer = models.ForeignKey('auth.User',
                                  verbose_name=_('organizer'))
    approved = models.BooleanField(verbose_name=_('registration approved'))

    def __unicode__(self):
        return (self.organizer.user.__unicode__() + unicode(_(" organizes ")) +
                self.competition.__unicode__())

    class Meta:
        ordering = ['added_at']
        verbose_name = _('organizer registration')
        verbose_name_plural = _('organizer registration')


class SeasonSeriesBaseMixin(object):

    def get_user_ranking(self, user):
        """
        Returns the user's ranking in the current series. Since user can be
        ranked on multiple places, e.g. if 3 users achieved the perfect score,
        the ranking is represented by a tuple (which would be (1,3) in this
        case). If only one user achieved perfect score, the resulting ranking
        would be (1,1).
        """

        results = self.results
        start = None
        end = 0
        user_total = None

        for i in range(0, len(results)):
            competitor, solutions, total = results[i]
            if user == competitor:
                start = end = i + 1
                user_total = total

            # This depends on the fact that the results list is sorted
            # decreasingly by the total score
            elif total == user_total:
                end = i + 1

            # If the start of the user interval is set, and we
            # don't have the same score, we stop searching
            elif start is not None:
                break

        return (start or 0, end)

    def get_user_percentile(self, user):
        """
        Returns user percentile (percentage of competitors that achieved
        worse or equal ranking), as a float between 0 and 1.
        """
        all_competitors = len(self.competitors)
        user_ranking = self.get_user_ranking(user)[0]

        # Percentile can be expressed as 1 - (percentage of better ranked users)
        return 1.0 - (user_ranking - 1) / float(all_competitors)

    def get_user_by_ranking(self, rank):
        """
        Returns the set of users at the given rank (which can be empty).
        """

        results = self.results

        # Convert rank to list index
        index = rank - 1

        users_at_rank = set()
        first_users_score = None

        if index < len(results):
            for competitor, solutions, total in results[index:]:

                # Mark the first user's score
                if first_users_score is None:
                    first_users_score = total

                # We add each user that has the same score until we reach
                # a lower score, at which point we break
                if total == first_users_score:
                    users_at_rank.add(competitor)
                else:
                    break

        return users_at_rank


@with_author
@with_timestamp
class Season(models.Model, SeasonSeriesBaseMixin):
    """
    Represents an one season of a competition. This is usually autumn or spring
    season. Using this model, however, we are not limited to 2 seasons per year.

    During each Season there might be several ProblemSets published as parts
    of that season.
    """

    competition = models.ForeignKey('competitions.Competition',
                                    verbose_name=_('competition'))
    year = models.IntegerField(verbose_name=_('year'))
    number = models.IntegerField(verbose_name=_('number'))
    name = models.CharField(max_length=50, verbose_name=_('name'))
    join_deadline = models.DateTimeField(blank=True,
                                         null=True,
                                         verbose_name=_('join deadline'))
    start = models.DateTimeField(verbose_name=_('season start'))
    end = models.DateTimeField(verbose_name=_('season end'))

    def get_year_segment(self, num_segments=2):
        """
        Returns the year segment this season belongs to.
        """

        season_midpoint = (self.start + (self.end - self.start) / 2).date()

        return YearSegment.by_date(season_midpoint, num_segments)

    @cached_property
    def num_problems(self):
        return sum(s.num_problems for s in self.series)

    @cached_property
    def series(self):
        """
        Provides a cached entry for all series.
        """
        return self.series_set.all()

    @cached_property
    def results(self):
        results = []

        series_results = [series.results for series in self.series]

        custom_total_func = getattr(settings,
                                    'ROOTS_SEASON_TOTAL_SCORE_FUNC',
                                    simple_series_solution_sum)

        season_results = []

        for competitor in self.competitors:
            user_results = [result_line[1:] for series_result in series_results for result_line in series_result
                            if result_line[0] == competitor]
            total = custom_total_func(user_results)

            season_results.append((competitor, user_results, total))

        season_results.sort(key=lambda x: x[2], reverse=True)
        return season_results


    @cached_property
    def competitors(self):
        """
        Returns the list of the competitors in the given season as everybody
        who submitted at least one problem solution in that season.
        """

        competitors = User.objects.none()

        for series in self.series_set.all():
            competitors = competitors | series.competitors

        return competitors

    def get_user_solutions(self, user):
        """
        Returns the list of lists of solutions of problems in this season
        for a particular user, each series in a separate list.

        If the problem was not submitted, None is used instead of a
        UserSolution object.
        """

        return [series.get_user_solutions(user)
                for series in self.series_set.all()]

    def get_user_solutions_with_total(self, user):
        """
        Returns a list of lists of user solutions with total score computed.

        Also gives a total score per season for this user. A total score may
        be computed using settings.ROOTS_TOTAL_SEASON_SCORE_FUNC. Fallbacks
        to a simple sum of series subtotals if not specified.
        """

        all_solutions = []
        total = 0

        for series in self.series_set.all():
            solutions, subtotal = series.get_user_solutions_with_total(user)
            all_solutions.append(solutions)
            total += subtotal

        custom_total_func = getattr(settings,
                                    'ROOTS_TOTAL_SEASON_SCORE_FUNC',
                                    None)

        if custom_total_func is not None:
            assert callable(custom_total_func)
            return custom_total_func(user, all_solutions)
        else:
            # Fallback to simple sum
            return all_solutions, total

    def get_series_nearest_deadline(self):
        """
        Returns the most relevant series for the deadline. That is usually the
        series which is still active, but closest to its deadline.

        If all series are past their deadline, returns the last series.
        If there are no series in this season, returns None.
        """

        active_series = self.series_set.filter(submission_deadline__gt=now())

        if active_series.exists():
            return active_series[0]
        else:
            if self.series_set.exists():
                return self.series_set.order_by('-submission_deadline')[0]
            else:
                return None

    def __unicode__(self):
        template = "{name} ({competition} {year}-{number})"
        return template.format(competition=remove_accents(self.competition),
                               year=self.year,
                               number=self.number,
                               name=remove_accents(self.name),
                               )

    class Meta:
        ordering = ['competition', 'year', 'number']
        verbose_name = _('Season')
        verbose_name_plural = _('Seasons')


@with_author
@with_timestamp
class Series(models.Model, SeasonSeriesBaseMixin):
    """
    Represents one series of problems in the season of the competition.
    """

    season = models.ForeignKey('competitions.Season',
                               verbose_name=_('season'))
    name = models.CharField(max_length=50,
                            verbose_name=_('name'))
    number = models.PositiveSmallIntegerField(verbose_name=_('number'))
    problemset = models.OneToOneField('problems.ProblemSet',
                                      blank=True,
                                      null=True,
                                      verbose_name=_('problem set assigned'))
    submission_deadline = models.DateTimeField(verbose_name=_('series submission deadline'))
    is_active = models.BooleanField(default=False,
                                    verbose_name=_('is series active'))

    @cached_property
    def num_problems(self):
        return self.problemset.problems.count()

    def sort_solutions(self, solutions):
        """
        Sorts the solutions passed as argument according to the order of the problems in the problemset.
        """

        sorted_solutions = [None] * self.num_problems
        problem_ids = list(self.problemset.problems.values_list('id', flat=True))

        for solution in solutions:
            try:
                sorted_solutions[problem_ids.index(solution.problem.pk)] = solution
            except ValueError:
                raise ValueError("Given solution %s is not for any problem in the problemset %s" %
                                 (solution, self.problemset))

        return sorted_solutions

    @cached_property
    def results(self):
        results = []

        # Fetch the UserSolution model manually, since importing causes cyclical imports
        UserSolution = get_model('problems', 'UserSolution')

        custom_total_func = getattr(settings,
                                    'ROOTS_SERIES_TOTAL_SCORE_FUNC',
                                    simple_solution_sum)

        series_problem_ids = self.problemset.problems.values_list('id', flat=True)

        solutions = (UserSolution.objects.only('problem', 'user', 'score', 'classlevel')
                                         .filter(problem__in=series_problem_ids)
                                         .order_by('user', 'problem')
                                         .select_related('user', 'problem'))

        current_user = None

        # Solutions are sorted by the user ids first, then by the problem ids
        for solution in solutions:
            if current_user != solution.user:
                # User has changed, compute the previous line if we are not processing the first solution
                if current_user is not None:
                    # Process the previous line
                    user_solutions = self.sort_solutions(user_solutions)
                    total = custom_total_func(user=current_user,
                                              solutions=user_solutions)
                    results.append((current_user, user_solutions, total))

                # Prepare the new result line
                current_user = solution.user
                user_solutions = [solution]
            else:
                user_solutions.append(solution)

        # Sort the results by total_score
        results.sort(key=lambda x: x[2], reverse=True)
        return results


    @cached_property
    def competitors(self):
        """
        Returns the list of the competitors in the given series as everybody
        who submitted at least one problem solution.
        """

        competitors = User.objects.filter(
                usersolution__problem__in=
                    self.problemset.problems.values_list('pk', flat=True)
            ).distinct()

        return competitors

    @cached_property
    def solutions(self):
        UserSolution = get_model('problems', 'UserSolution')
        series_problem_ids = self.problemset.problems.values_list('id', flat=True)
        return UserSolution.objects.filter(problem__in=series_problem_ids)

    def get_user_solutions(self, user):
        """
        Returns the list of solutions of problems in this series for a
        particular user. If the problem was not submitted, None is used
        instead of a UserSolution object.
        """

        solutions = self.solutions.filter(user=user)
        return self.sort_solutions(solutions)

    def get_user_solutions_with_total(self, user):
        """
        Returns a list of user solutions with total score computed.

        The computation of the total score can follow any arbitrary rules,
        it needs to be specified by the settings.ROOTS_SERIES_TOTAL_SCORE_FUNC.

        This defaults to simple sum.
        """

        solutions = self.get_user_solutions(user)

        custom_total_func = getattr(settings,
                                    'ROOTS_SERIES_TOTAL_SCORE_FUNC',
                                    simple_solution_sum)

        return solutions, custom_total_func(user, solutions)

    def is_past_submission_deadline(self):
        return now() > self.submission_deadline

    def is_nearest_deadline(self):
        # Series are returned sorted by the submission deadline
        return self == self.season.get_series_nearest_deadline()

    def clean(self, *args, **kwargs):
        if self.is_active:
            if not self.submission_deadline:
                raise ValidationError("Submission deadline must be set to "
                                      "make the series active")
            if not self.problemset:
                raise ValidationError("Corresponding set of problems must be "
                                      "set to make the series active")

            if self.is_past_submission_deadline():
                raise ValidationError("Series that is past its submission "
                                      "deadline cannot be made active")

        super(Series, self).clean(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:

        ordering = ['submission_deadline']
        unique_together = ('season', 'number')
        verbose_name = _('Series')
        verbose_name_plural = _('Series')
