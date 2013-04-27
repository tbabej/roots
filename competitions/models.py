from django.db import models
from django.contrib import admin


# Competition-related models
class Competition(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class CompetitionUserRegistration(models.Model):
    competition = models.ForeignKey('competitions.Competition')
    user = models.ForeignKey('users.User')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" competes in " +
               self.competition.__unicode__())


class CompetitionOrgRegistration(models.Model):
    competition = models.ForeignKey('competitions.Competition')
    organizer = models.ForeignKey('users.Organizer')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" organizes " +
               self.competition.__unicode__())

# Register to the admin site
admin.site.register(Competition)
admin.site.register(CompetitionUserRegistration)
admin.site.register(CompetitionOrgRegistration)