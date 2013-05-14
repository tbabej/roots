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

    # Fields inherited from AuthUser:

    # username
    # first_name
    # last_name
    # email
    # password
    # is_staff
    # is_active
    # is_superuser
    # last_login
    # date_joined

    date_of_birth = models.DateTimeField(blank=True)
    sex = models.CharField(max_length=1, blank=True, choices=(('M', 'male'),
                                                              ('F', 'female')))
    social_security_number = models.CharField(max_length=11, blank=True)
    state_id_number = models.CharField(max_length=7, blank=True)

    competes = models.ManyToManyField('competitions.Competition',
                    through='competitions.CompetitionUserRegistration')

    # address information
    phone_number = models.CharField(max_length=30, blank=True)
    parent_phone_number = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_number = models.CharField(max_length=10, blank=True)
    region = models.CharField(max_length=30, blank=True,
                              choices=(('KE', 'Kosicky'),
                                       ('PR', 'Presovsky'),
                                       ('BB', 'Banskobystricky'),
                                       ('BA', 'Bratislavsky'),
                                       ('ZI', 'Zilinsky'),
                                       ('TC', 'Trenciansky'),
                                       ('TV', 'Trnavsky'),
                                       ('NI', 'Nitriansky')))

    # TODO: add school model? we need school address anyway
    school_class = models.CharField(max_length=20, blank=True)
    school = models.CharField(max_length=100, blank=True)
    classlevel = models.CharField(max_length=2, blank=True,
                                  choices=(('Z2', 'Z2'),
                                           ('Z3', 'Z3'),
                                           ('Z4', 'Z4'),
                                           ('Z5', 'Z5'),
                                           ('Z6', 'Z6'),
                                           ('Z7', 'Z7'),
                                           ('Z8', 'Z8'),
                                           ('Z9', 'Z9'),
                                           ('S1', 'S1'),
                                           ('S2', 'S2'),
                                           ('S3', 'S3'),
                                           ('S4', 'S4')))

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
