from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from base.util import with_timestamp, with_author

# Competition-related models
@with_author
@with_timestamp
class Competition(models.Model):
    """
    Represents a competition. One roots site will usually hold several
    competitions, as there are usually several age categories or several
    subjects categories. Or both.
    """

    name = models.CharField(max_length=100)

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

    class Meta:
        ordering = ['name']
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'


@with_author
@with_timestamp
class CompetitionUserRegistration(models.Model):
    """
    Represents a relation between user and competition. User himself can
    register into competition if he satisfies the conditions.
    """

    competition = models.ForeignKey('competitions.Competition')
    user = models.ForeignKey('profiles.UserProfile')

    def __unicode__(self):
        return (self.user.__unicode__() + u" competes in " +
               self.competition.__unicode__())

    class Meta:
        ordering = ['added_at']
        verbose_name = 'User registration'
        verbose_name_plural = 'User registrations'


@with_author
@with_timestamp
class CompetitionOrgRegistration(models.Model):
    """
    Represents a relation between organizer and comeptition. Organizer can
    help organize multiple competitions. Organizer registrations have to
    be approved.
    """

    competition = models.ForeignKey('competitions.Competition')
    organizer = models.ForeignKey('profiles.UserProfile')
    approved = models.BooleanField()

    def __unicode__(self):
        return (self.organizer.__unicode__() + u" organizes " +
               self.competition.__unicode__())

    class Meta:
        ordering = ['added_at']
        verbose_name = 'Organizer registration'
        verbose_name_plural = 'Organizer registration'


@with_author
@with_timestamp
class Season(models.Model):
    """
    Represents an one season of a competition. This is usually autumn or spring
    season. Using this model, however, we are not limited to 2 seasons per year.

    During each Season there might be several ProblemSets published as parts
    of that season.
    """

    competition = models.ForeignKey('competitions.Competition')
    year = models.IntegerField()
    number = models.IntegerField()
    name = models.CharField(max_length=50)
    join_deadline = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        template = "{name} ({competition} {year}-{number})"
        return template.format(competition=unicode(self.competition),
                               year=self.year,
                               number=self.number,
                               name=self.name,
                               )

    class Meta:
        ordering = ['competition', 'year', 'number']
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'


@with_author
@with_timestamp
class Series(models.Model):
    """
    Represents one series of problems in the season of the competetion.
    """

    season = models.ForeignKey('competitions.Season')
    name = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField()
    problemset = models.OneToOneField('problems.ProblemSet', blank=True,
                                      null=True)
    submission_deadline = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def is_past_submission_deadline(self):
        return now() > self.submission_deadline

    def is_nearest_deadline(self):
        # Series are returned sorted by the submission deadline
        active_series = [s for s in Series.objects.all()
                           if not s.is_past_submission_deadline()]

        if active_series:
            return active_series[0] == self
        else:
            return False

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
        verbose_name = 'Series'
        verbose_name_plural = 'Series'
