from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from base.util import with_timestamp, with_author, remove_accents


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
                            verbose_name=_('competition name'))
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

    def get_active_season(self):
        season_candidates = self.season_set.filter(start__lt=now(),
                                                   end__gt=now())
        if season_candidates.exists():
            return season_candidates[0]
        else:
            return None

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
    user = models.ForeignKey('profiles.UserProfile',
                             verbose_name=_('user'))

    def __unicode__(self):
        return (self.user.__unicode__() + u" competes in " +
               self.competition.__unicode__())

    class Meta:
        ordering = ['added_at']
        verbose_name = _('user registration')
        verbose_name_plural = _('user registrations')


@with_author
@with_timestamp
class CompetitionOrgRegistration(models.Model):
    """
    Represents a relation between organizer and comeptition. Organizer can
    help organize multiple competitions. Organizer registrations have to
    be approved.
    """

    competition = models.ForeignKey('competitions.Competition',
                                    verbose_name=_('competition'))
    organizer = models.ForeignKey('profiles.UserProfile',
                                  verbose_name=_('organizer'))
    approved = models.BooleanField(verbose_name=_('registration approved'))

    def __unicode__(self):
        return (self.organizer.__unicode__() + _(" organizes ") +
               self.competition.__unicode__())

    class Meta:
        ordering = ['added_at']
        verbose_name = _('organizer registration')
        verbose_name_plural = _('organizer registration')


@with_author
@with_timestamp
class Season(models.Model):
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

    def get_competitors(self):
        """
        Returns the list of the competitors in the given season as everybody
        who submitted at least one problem solution in that season.
        """

        competitors = User.objects.none()

        for series in self.series_set.all():
            competitors = competitors | series.get_competitors()

        return competitors

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
class Series(models.Model):
    """
    Represents one series of problems in the season of the competetion.
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
    submission_deadline = models.DateTimeField(
                              verbose_name=_('series submission deadline'))
    is_active = models.BooleanField(default=False,
                                    verbose_name=_('is series active'))

    def get_competitors(self):
        """
        Returns the list of the competitors in the given series as everybody
        who submitted at least one problem solution.
        """

        competitors = User.objects.none()

        for problem in self.problemset.problems.all():
            problemset_competitors = User.objects.filter(
                usersolution__pk__in=problem.usersolution_set.all())
            competitors = competitors | problemset_competitors

        return competitors.distinct()

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

        super(Series, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:

        ordering = ['submission_deadline']
        unique_together = ('season', 'number')
        verbose_name = _('Series')
        verbose_name_plural = _('Series')
