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

    def __unicode__(self):
        return self.name


class CompetitionUserRegistration(models.Model):
    """
    Represents a relation between user and competition. User himself can
    register into competition if he satisfies the conditions.
    """

    competition = models.ForeignKey('competitions.Competition')
    user = models.ForeignKey('users.User')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" competes in " +
               self.competition.__unicode__())


class CompetitionOrgRegistration(models.Model):
    """
    Represents a relation between organizer and comeptition. Organizer can
    help organize multiple competitions. Organizer registrations have to
    be approved.
    """

    competition = models.ForeignKey('competitions.Competition')
    organizer = models.ForeignKey('users.Organizer')
    timestamp = models.DateTimeField()
    approved = models.BooleanField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" organizes " +
               self.competition.__unicode__())


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

# Register to the admin site
admin.site.register(Competition)
admin.site.register(CompetitionUserRegistration)
admin.site.register(CompetitionOrgRegistration)
admin.site.register(Season)