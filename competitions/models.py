import datetime
from operator import or_
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
    organizer_group = models.ForeignKey('auth.Group',
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

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

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
        it occurred.

        Returns (None, None) if no user ranking found (user would have to never
        submit a solution).
        """

        best_rank = None
        best_season = None

        for season in self.get_all_user_seasons(user):
            rank, _ = season.get_user_ranking(user)
            if rank < best_rank:
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

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return ("user__name__icontains", "competition__name__icontains")

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
    approved = models.BooleanField(verbose_name=_('registration approved'),
                                   default=False)

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return ("organizer__name__icontains", "competition__name__icontains")

    def __unicode__(self):
        return (self.organizer.__unicode__() + unicode(_(" organizes ")) +
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
        current_total = None
        user_in_this_interval = False

        for i in range(0, len(results)):
            competitor, solutions, total, registration = results[i]

            # Compute the start and end of the interval of users with the same score
            if total != current_total:
                if user_in_this_interval:
                    return (start, end)
                else:
                    start = end = i + 1
                    current_total = total
            else:
                end = i + 1

            # Make a note if user was found in this interval
            if competitor == user:
                user_in_this_interval = True

        # We get here only if the queried user belongs to the last tier
        return (start, end) if user_in_this_interval else (None, None)

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
            for competitor, solutions, total, registration in results[index:]:

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

    @cached_property
    def results_with_ranking(self):
        results = self.results

        new_results = []
        for row in results:
            rank = self.get_user_ranking(row[0])
            new_results.append(row + (rank,))

        return new_results


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
    sum_method = models.CharField(max_length=50,
                                  blank=True,
                                  null=True,
                                  help_text=_('Method that is used to compute the sum of the season'),
                                  choices=settings.ROOTS_SEASON_TOTAL_SUM_METHOD_CHOICES)

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
    def problems(self):
        # Fetch the problem model, since we cannot import due circular
        # dependencies
        Problem = get_model('problems', 'Problem')

        # Find all problems for all series in this season
        all_problems = [
            series.problems.all()
            for series in self.series_set.all()
        ]

        # Return union of those problemsets
        return reduce(or_, all_problems, Problem.objects.none())

    @cached_property
    def series(self):
        """
        Provides a cached entry for all series.
        """
        return self.series_set.all()

    @cached_property
    def active_series(self):
        """
        Returns all the series that are active (before their submussion
        deadline).
        """

        return self.series_set.filter(submission_deadline__gt=now())

    @cached_property
    def finished_series(self):
        """
        Returns all the series that are after their submission deadline
        """

        return self.series_set.filter(submission_deadline__lt=now())

    @cached_property
    def registrations(self):
        # Keep registrations in a dict for performance
        return {
            registration.user.pk: registration for registration in
            self.userseasonregistration_set.all().select_related('user', 'school')
            }

    @cached_property
    def results(self):
        custom_total_func = getattr(settings,
                                    self.sum_method or '',
                                    simple_series_solution_sum)

        season_results = []

        for competitor in self.competitors:
            user_results = []
            for series in self.series:
                # Find the user's line in the results table
                matching_lines = [line[1:] for line in series.results
                                  if line[0] == competitor]

                # There should be at most one line matching the user's name
                # in the results table. If there is none, make a empty line.
                if matching_lines:
                    user_result = matching_lines[0][:-1]
                else:
                    user_result = ([None] * series.num_problems, 0)

                user_results.append(user_result)

            total = custom_total_func(user_results)
            season_results.append((competitor, user_results, total,
                                   self.registrations[competitor.pk]))

        season_results.sort(key=lambda x: x[2], reverse=True)
        return season_results

    @property
    def solutions(self):
        # Fetch the UserSolution model manually, since importing causes cyclical imports
        UserSolution = get_model('problems', 'UserSolution')
        return reduce(or_, [series.solutions for series in self.series], UserSolution.objects.none())

    @property
    def not_corrected_solutions(self):
        # Fetch the UserSolution model manually, since importing causes cyclical imports
        UserSolution = get_model('problems', 'UserSolution')
        return reduce(or_, [series.not_corrected_solutions for series in self.series], UserSolution.objects.none())

    @property
    def is_over(self):
        return self.not_corrected_solutions.count() == 0

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
        be computed using settings.<self.sum_method>. Fallbacks
        to a simple sum of series subtotals if not specified.
        """

        all_solutions = []
        total = 0

        for series in self.series_set.all():
            solutions, subtotal = series.get_user_solutions_with_total(user)
            all_solutions.append(solutions)
            total += subtotal

        custom_total_func = getattr(settings,
                                    self.sum_method or '',
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

        if self.active_series.exists():
            # Series are sorted by the submission deadline, so return
            # the first that is not over yet
            return self.active_series[0]
        else:
            # If all the series are over, just return the last one
            if self.series_set.exists():
                return self.series_set.order_by('-submission_deadline')[0]
            else:
                return None

    def get_first_series_after_deadline(self):
        """
        Returns the most relevant series after the deadline. That is usually the
        series which just finished.

        If no series are past their deadline, returns the first series.
        If there are no series in this season, returns None.
        """

        if self.finished_series.exists():
            # Series are ordered by their submission deadline, so we need
            # to reverse the ordering
            return self.finished_series.order_by('-submission_deadline')[0]
        else:
            # If no series finished yet, simply return the first series
            if self.series_set.exists():
                return self.series_set.all()[0]
            else:
                return None

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains", "competition__name__icontains",
                "year__iexact", "number__iexact")

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
    sum_method = models.CharField(max_length=50,
                                  blank=True,
                                  null=True,
                                  verbose_name=_('total method'),
                                  help_text=_('Method that is used to compute the sum of the series'),
                                  choices=settings.ROOTS_SERIES_TOTAL_SUM_METHOD_CHOICES)

    @cached_property
    def num_problems(self):
        return self.problems.count()

    @cached_property
    def problems(self):
        return self.problemset.problems.all()

    @cached_property
    def problems_ids(self):
        return list(self.problems.values_list('id', flat=True))

    @property
    def time_to_deadline(self):
        """
        Returns the remaining time to the submission deadline as a datetime.timedelta object. If the deadline is over,
        returns datetime.timedelta(0).
        """
        remaining_time = self.submission_deadline - now()

        if remaining_time.total_seconds() < 0:
            return datetime.timedelta(0)
        else:
            return remaining_time

    def get_elapsed_time_percentage(self, base_timespan=datetime.timedelta(30)):
        """
        Returns the remaining time percentage for the given series. The
        base_timespan parameter defines the time when the countdown starts
        (by default 30 days before the submission deadline).
        """

        remaining_time = self.time_to_deadline

        # If the remaining time is more than base_timespan, return 0 percent
        # to prevent negative values
        if remaining_time > base_timespan:
            return 0
        else:
            elapsed = (
                remaining_time.total_seconds() / base_timespan.total_seconds()
            )

            return (1.0 - elapsed) * 100

    def sort_solutions(self, solutions):
        """
        Sorts the solutions passed as argument according to the order of the
        problems in the problemset.
        """

        sorted_solutions = [None] * self.num_problems

        for solution in solutions:
            try:
                sorted_solutions[self.problems_ids.index(solution.problem.pk)] = solution
            except ValueError:
                raise ValueError("Given solution %s is not for any problem in the problemset %s" %
                                 (solution, self.problemset))

        return sorted_solutions

    @cached_property
    def results(self):
        results = []

        # Fetch the UserSolution model manually, since importing causes cyclical imports
        UserSolution = get_model('problems', 'UserSolution')
        UserSeasonRegistration = get_model('profiles', 'UserSeasonRegistration')

        custom_total_func = getattr(settings,
                                    (self.sum_method or ''),
                                    simple_solution_sum)

        solutions = (UserSolution.objects.only('problem', 'user', 'score', 'classlevel')
                                         .filter(problem__in=self.problems_ids)
                                         .order_by('user', 'problem')
                                         .select_related('user', 'problem'))

        current_user = None

        # Solutions are sorted by the user ids first, then by the problem ids
        for solution in solutions:
            if current_user != solution.user:
                # User has changed, compute the previous line if we are not processing the first solution
                if current_user is not None:
                    # Find the current user's registration to the given season
                    registration = self.season.registrations[current_user.pk]

                    # Process the previous line
                    user_solutions = self.sort_solutions(user_solutions)
                    total = custom_total_func(user=current_user,
                                              registration=registration,
                                              solutions=user_solutions)
                    results.append((current_user, user_solutions, total,
                                    registration))

                # Prepare the new result line
                current_user = solution.user
                user_solutions = [solution]
            else:
                user_solutions.append(solution)

        # Process the last user
        if current_user is not None:
            # Find the current user's registration to the given season
            registration = self.season.registrations[current_user.pk]

            user_solutions = self.sort_solutions(user_solutions)
            total = custom_total_func(user=current_user,
                                      solutions=user_solutions)
            results.append((current_user, user_solutions, total, registration))

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
                usersolution__problem__in=self.problems_ids
            ).distinct()

        return competitors

    @cached_property
    def solutions(self):
        UserSolution = get_model('problems', 'UserSolution')
        return UserSolution.objects.filter(problem__in=self.problems_ids)

    @property
    def not_corrected_solutions(self):
        return self.solutions.filter(score=None)

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
        it needs to be specified by the settings.<self.sum_method>.

        This defaults to simple sum.
        """

        UserSeasonRegistration = get_model('profiles', 'UserSeasonRegistration')
        solutions = self.get_user_solutions(user)

        custom_total_func = getattr(settings,
                                    self.sum_method or '',
                                    simple_solution_sum)

        # Fint the current user's registration to the given season
        registration = UserSeasonRegistration.objects.get(
            user=user, season=self.season)

        # Process the previous line
        total = custom_total_func(user=current_user,
                                  registration=registration,
                                  solutions=user_solutions)

        return solutions, total

    def is_past_submission_deadline(self):
        return now() > self.submission_deadline

    def is_nearest_deadline(self):
        # Series are returned sorted by the submission deadline
        return self == self.season.get_series_nearest_deadline()

    def is_first_past_deadline(self):
        return self == self.season.get_first_series_after_deadline()

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

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

    def __unicode__(self):
        return self.name

    class Meta:

        ordering = ['submission_deadline']
        unique_together = ('season', 'number')
        verbose_name = _('Series')
        verbose_name_plural = _('Series')
