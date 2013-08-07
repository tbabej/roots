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

    registered_user = models.ManyToManyField('auth.User',
                                             through='EventUserRegistration')
    registered_org = models.ManyToManyField('auth.User',
                                            through='EventOrgRegistration',
                                            related_name='organized_event_set')

    # Fields added via foreign keys:

    #  gallery_set

    # Fields added via inheritance:

    #  camp

    def __unicode__(self):
        return self.name


class EventUserRegistration(models.Model):
    """
    Represents a user's registration to the event.
    """

    event = models.ForeignKey('events.Event')
    user = models.ForeignKey('auth.User')
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
    organizer = models.ForeignKey('auth.User')
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

    Attribute invitation_deadline holds the deadline for accepting invitations.
    """

    invited = models.ManyToManyField('auth.User',
                                     through='events.CampUserInvitation')
    invitation_deadline = models.DateTimeField()

    # Fields added via inheritance:

    #  event_ptr

    def __unicode__(self):
        return self.location


class CampUserInvitation(models.Model):
    """
    Represents an invitation to the given camp for the given user.

    User's can be invited either as regular participants or substitutes.'

    All users that satisfy given competition's conditions (e.g thay gain
    sufficient amount of points in the season) should be invited at least
    as substitutes.

    An information about user's order (priority) is kept.
    """

    INVITATION_TYPES = (('REG', 'regular'), ('SUB', 'substitute'))

    user = models.ForeignKey('auth.User')
    camp = models.ForeignKey('events.Camp')
    invited_as = models.CharField(max_length=3, choices=INVITATION_TYPES)
    order = models.IntegerField()
    user_accepted = models.BooleanField(default=False)
    user_accepted_timestamp = models.DateTimeField()

    def __unicode__(self):
        return (self.user.__unicode__() + u' was invited to '
                + self.camp.__unicode())

    # TODO: invitation should hold requirements on user profile contents
    #       e.g. to attend a camp one should have some sort of contact filled
    #       in the profile

# Register to the admin site
admin.site.register(Event)
admin.site.register(EventUserRegistration)
admin.site.register(EventOrgRegistration)
admin.site.register(Camp)
