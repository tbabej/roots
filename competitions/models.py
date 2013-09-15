from django.db import models
from django.contrib import admin


# Competition-related models
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


class CompetitionUserRegistration(models.Model):
    """
    Represents a relation between user and competition. User himself can
    register into competition if he satisfies the conditions.
    """

    competition = models.ForeignKey('competitions.Competition')
    user = models.ForeignKey('profiles.UserProfile')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.user.__unicode__() + u" competes in " +
               self.competition.__unicode__())

    class Meta:
        ordering = ['added_at']
        verbose_name = 'User registration'
        verbose_name_plural = 'User registrations'


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
        return (self.user.__unicode__() + u" organizes " +
               self.competition.__unicode__())

    class Meta:
        ordering = ['added_at']
        verbose_name = 'Organizer registration'
        verbose_name_plural = 'Organizer registration'


class Season(models.Model):
    """
    Represents an one season of a competition. This is usually autumn or spring
    season. Using this model, however, we are no limited to 2 seasons per year.

    During each Season there might be several ProblemSets published as parts
    of that season.
    """

    competition = models.ForeignKey('competitions.Competition')
    year = models.IntegerField()
    number = models.IntegerField()
    name = models.CharField(max_length=50)

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


class Series(models.Model):
    """
    Represents one series of problems in the season of the competetion.
    """

    #TODO: add validator that makes it impossoble to make season active unless
    #      submission deadline and problemset are set

    season = models.ForeignKey('competitions.Season')
    name = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField()
    problemset = models.OneToOneField('problems.ProblemSet', blank=True,
                                      null=True)
    submission_deadline = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:

        ordering = ['submission_deadline']
        unique_together = ('season', 'number')
        verbose_name = 'Series'
        verbose_name_plural = 'Series'


# Register to the admin site
admin.site.register(Competition)
admin.site.register(CompetitionUserRegistration)
admin.site.register(CompetitionOrgRegistration)
admin.site.register(Season)
admin.site.register(Series)
