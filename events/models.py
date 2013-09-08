from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from base.util import with_timestamp, with_author


# Event-related models
@with_author
@with_timestamp
class Event(models.Model):
    """
    Event represents a simple event, that is opened to public. This can be
    either a public presentation, or a public game.

    Users are not invited, but can notify the organizer that they want to
    participate. This relation is represented using EventUserRegistration.
    """

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registration_end_time = models.DateTimeField(
                                blank=True,
                                null=True,  # default is set in save() method
                                validators=[MaxValueValidator(start_time)],
                                )

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

    def get_num_users(self):
        return self.registered_user.count()
    get_num_users.short_description = 'Users attending:'

    def get_num_orgs(self):
        return self.registered_org.count()
    get_num_orgs.short_description = 'Organizers attending:'

    def started(self):
        return self.start_time < now()

    def ended(self):
        return self.end_time < now()

    def registration_open(self):
        return now() < self.registration_end_time

    def in_progress(self):
        return self.started() and not self.ended()

    def register_user(self, user):
        if self.registration_open():
            registration = EventUserRegistration(event=self, user=user)
            registration.save()
        else:
            raise ValidationError("Cannot register  user {user} to event "
                                  "{event}: Registration ended at {end}"
                                  .format(user=user, event=self,
                                          end=self.registration_end_time)
                                 )

    def save(self, *args, **kwargs):
        if not self.registration_end_time:
            self.registration_end_time = self.start_time
        super(Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ['start_time', 'end_time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


@with_timestamp
class EventUserRegistration(models.Model):
    """
    Represents a user's registration to the event.
    """

    event = models.ForeignKey('events.Event')
    user = models.ForeignKey('auth.User')

    def __unicode__(self):
        return (self.user.__unicode__() + u" goes to " +
               self.event.__unicode__())

    class Meta:
        order_with_respect_to = 'event'
        verbose_name = 'User registration'
        verbose_name_plural = 'User registrations'


@with_timestamp
class EventOrgRegistration(models.Model):
    """
    Represents a organizer's registration to the event. This is merely for them
    to let everybody know that they will be available (if help with organization
    is needed).
    """

    event = models.ForeignKey('events.Event')
    organizer = models.ForeignKey('auth.User')

    def __unicode__(self):
        return (self.user.__unicode__() + u" organizes " +
               self.event.__unicode__())

    class Meta:
        order_with_respect_to = 'event'
        verbose_name = 'Organizer registration'
        verbose_name_plural = 'Organizer registrations'


@with_author
@with_timestamp
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
    invitation_deadline = models.DateTimeField(blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    season = models.ForeignKey('competitions.Season', blank=True, null=True)

    # Fields added via inheritance:

    #  event_ptr

    def get_num_users_invited(self):
        return self.invited.count()
    get_num_users_invited.short_description = "Number of invited users"

    def get_users_signed(self):
        return (self.invited
                .filter(campuserinvitation__user_accepted=True)
            )

    def get_num_users_signed(self):
        return self.get_users_signed().count()
    get_num_users_signed.short_description = "Number of users that signed"

    def get_users_accepted(self):
        return (self.get_users_signed()
            .filter(campuserinvitation__org_accepted=True)
            )

    def get_num_users_accepted(self):
        return self.get_users_accepted().count()
    get_num_users_accepted.short_description = "Number of users were accepted"

    class Meta:
        verbose_name = 'Camp'
        verbose_name_plural = 'Camps'


@with_timestamp
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
    org_accepted = models.BooleanField(default=False)

    def __unicode__(self):
        return (self.user.__unicode__() + u' was invited to '
                + self.camp.__unicode())

    # TODO: invitation should hold requirements on user profile contents
    #       e.g. to attend a camp one should have some sort of contact filled
    #       in the profile

    class Meta:
        order_with_respect_to = 'camp'
        verbose_name = 'Camp invitation'
        verbose_name_plural = 'Camp invitations'
