from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User as AuthUser


# User-related models
class User(AuthUser):
    '''
    Represents an user. Both organizers and participants are considered as
    users. This allows usage of the same accounts for the users that became
    organizers later.
    '''

    login = models.CharField(max_length=50)
    competes = models.ManyToManyField('competitions.Competition',
                    through='competitions.CompetitionUserRegistration')
    #  TODO this is not designed well, needs extra parameters on this relation
    solved = models.ManyToManyField('problems.Problem')

    # Fields added via foreign keys:

    #  camp_set
    #  campuserinvitation_set
    #  competitionuserregistration_set
    #  event_set
    #  eventuserregistration_set
    #  usersolution_set

    # Fields added via inheritance:

    #  organizer

    def __unicode__(self):
        return self.login


class Organizer(User):
    '''
    Represents an organizer. Organizer can organize multiple competitions
    or events.
    '''

    motto = models.CharField(max_length=50)

    # TODO: there are 2 data descriptors added via many-to-many relationship
    #       in this case it's organized_event_set (custom name due to
    #       the fact that optional parameter related_name was defined)
    #       and eventorgregistration_set
    #       Investigate!

    # Fields added via foreign keys:

    #  competitionorgregistration_set
    #  eventorgregistration_set
    #  organized_event_set
    #  registeredorg
    #  orgsolution_set
    #  post_set

    # Fields added via inheritance:

    #  user_ptr


# Register to the admin site
admin.site.register(User)
admin.site.register(Organizer)
