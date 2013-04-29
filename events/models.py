from django.db import models
from django.contrib import admin


# Event-related models
class Event(models.Model):
    """
    Event represents a simple event, that is opened to public. This can be
    either a public presentation, or a public game.

    Users are not invited, but can notify the organizer that they want to
    participate. This relation is represented using EventUserRegistration.
    """

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    galerry = models.ForeignKey('posts.Gallery')
    registered_user = models.ManyToManyField('users.User',
                                             through='EventUserRegistration')
    registered_org = models.ManyToManyField('users.Organizer',
                                            through='EventOrgRegistration',
                                            related_name='organizers')

    def __unicode__(self):
        return self.name


class EventUserRegistration(models.Model):
    """
    Represents a user's registration to the event.'
    """

    event = models.ForeignKey('events.Event')
    user = models.ForeignKey('users.User')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" goes to " +
               self.event.__unicode__())


class EventOrgRegistration(models.Model):
    """
    Represents a organizer's registration to the event. This is merely for them
    to let everybody know that they will be available (if help with organization
    is needed).
    """

    event = models.ForeignKey('events.Event')
    organizer = models.ForeignKey('users.Organizer')
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u" organizes " +
               self.event.__unicode__())


class Camp(Event):
    """
    This class is called Camp from historical reasons. It is supposed to model
    an workshop that is open only to the best of the competitors in the given
    competition's season.

    User's have to be invited to be able to register. Usually more users than
    the capacity allows are invited, some are substitutes.'
    """

    location = models.CharField(max_length=100)  # temporary placeholder

    def __unicode__(self):
        return self.location


# Register to the admin site
admin.site.register(Event)
admin.site.register(EventUserRegistration)
admin.site.register(EventOrgRegistration)
admin.site.register(Camp)