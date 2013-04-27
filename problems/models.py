from django.db import models
from django.contrib import admin


# Solution-related models
class UserSolution(models.Model):
    user = models.ForeignKey('users.User')
    problem = models.ForeignKey('problems.Problem')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.user.__unicode__() + u":'s solution of " +
                self.problem.__unicode__())


class OrgSolution(models.Model):
    organizer = models.ForeignKey('users.Organizer')
    problem = models.ForeignKey('problems.Problem')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.user.__unicode__() + u":'s ideal solution of " +
                self.problem.__unicode__())


# Problem-related models
class Problem(models.Model):
    text = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.text


class ProblemSet(models.Model):
    competition = models.ForeignKey('competitions.Competition',
                                    blank=True, null=True)
    leaflet = models.ForeignKey('leaflets.Leaflet',
                                blank=True, null=True)
    problems = models.ManyToManyField(Problem)

    def __unicode__(self):
        return u"ProblemSet for " + self.competition.__unicode__()

# Register to the admin site
admin.site.register(Problem)
admin.site.register(ProblemSet)
admin.site.register(UserSolution)
admin.site.register(OrgSolution)