from django.db import models


# Competition-related models
class Competition(models.Model):
    name = models.CharField(max_length=100)


class CompetitionUserRegistration(models.Model):
    competition = models.ForeignKey('Competition')
    user = models.ForeignKey('User')
    timestamp = models.DateTimeField()


class CompetitionOrgRegistration(models.Model):
    competition = models.ForeignKey('Competition')
    organizer = models.ForeignKey('Organizer')
    timestamp = models.DateTimeField()


# User-related models
class User(models.Model):
    login = models.CharField(max_length=50)
    competes = models.ManyToManyField('Competition',
                                      through='CompetitionUserRegistration')
    solved = models.ManyToManyField('Problem')


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


class EventUserRegistration(models.Model):
    event = models.ForeignKey('Event')
    user = models.ForeignKey('User')
    timestamp = models.DateTimeField()


class EventOrgRegistration(models.Model):
    event = models.ForeignKey('Event')
    organizer = models.ForeignKey('Organizer')
    timestamp = models.DateTimeField()


class Camp(Event):
    location = models.CharField(max_length=100)  # temporary placeholder


# Solution-related models
class UserSolution(models.Model):
    user = models.ForeignKey('User')
    problem = models.ForeignKey('Problem')
    timestamp = models.DateTimeField(auto_now_add=True)


class OrgSolution(models.Model):
    organizer = models.ForeignKey('Organizer')
    problem = models.ForeignKey('Problem')
    timestamp = models.DateTimeField(auto_now_add=True)


# Problem-related models
class Problem(models.Model):
    text = models.CharField(max_length=1000)


class ProblemSet(models.Model):
    competition = models.ForeignKey('Competition', blank=True, null=True)
    leaflet = models.ForeignKey('Leaflet', blank=True, null=True)
    problems = models.ManyToManyField('Problem')


class Leaflet(models.Model):
    competition = models.ForeignKey('Competition')
    year = models.IntegerField()


# Content-related models
class Post(models.Model):
    organizer = models.ForeignKey('Organizer')
    title = models.CharField(max_length=100)


class Gallery(models.Model):
    name = models.CharField(max_length=50)