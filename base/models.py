from django.db import models


# Competition-related models
class Competition(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class CompetitionUserRegistration(models.Model):
    competition = models.ForeignKey('Competition')
    user = models.ForeignKey('User')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" competes in " +
               self.competition.__unicode__())


class CompetitionOrgRegistration(models.Model):
    competition = models.ForeignKey('Competition')
    organizer = models.ForeignKey('Organizer')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" organizes " +
               self.competition.__unicode__())


# User-related models
class User(models.Model):
    login = models.CharField(max_length=50)
    competes = models.ManyToManyField('Competition',
                                      through='CompetitionUserRegistration')
    solved = models.ManyToManyField('Problem')

    def __unicode__(self):
        return self.login


class Organizer(User):
    motto = models.CharField(max_length=50)


# Event-related models
class Event(models.Model):
    name = models.CharField(max_length=100)
    galerry = models.ForeignKey('Gallery')
    registered_user = models.ManyToManyField('User',
                                             through='EventUserRegistration')
    registered_org = models.ManyToManyField('Organizer',
                                            through='EventOrgRegistration',
                                            related_name='organizers')

    def __unicode__(self):
        return self.name


class EventUserRegistration(models.Model):
    event = models.ForeignKey('Event')
    user = models.ForeignKey('User')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" goes to " +
               self.event.__unicode__())


class EventOrgRegistration(models.Model):
    event = models.ForeignKey('Event')
    organizer = models.ForeignKey('Organizer')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" organizes " +
               self.event.__unicode__())


class Camp(Event):
    location = models.CharField(max_length=100)  # temporary placeholder

    def __unicode__(self):
        return self.location


# Solution-related models
class UserSolution(models.Model):
    user = models.ForeignKey('User')
    problem = models.ForeignKey('Problem')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return (self.user.__unicode__() + u":'s solution of " +
                self.problem.__unicode__())


class OrgSolution(models.Model):
    organizer = models.ForeignKey('Organizer')
    problem = models.ForeignKey('Problem')
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
    competition = models.ForeignKey('Competition', blank=True, null=True)
    leaflet = models.ForeignKey('Leaflet', blank=True, null=True)
    problems = models.ManyToManyField('Problem')

    def __unicode__(self):
        return u"RpoblemSet for " + self.competition.__unicode__()


class Leaflet(models.Model):
    competition = models.ForeignKey('Competition')
    year = models.IntegerField()

    def __unicode__(self):
        return u"Leaflet for " + self.competition.__unicode__()


# Content-related models
class Post(models.Model):
    organizer = models.ForeignKey('Organizer')
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title


class Gallery(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
