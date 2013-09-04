from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


# User-related models
class UserProfile(models.Model):
    '''
    Represents an user profile. This contains non-auth information stored
    for the particular user.

    Any user can have both UserProfile and OrganizerProfile set.
    '''

    # Fields accessible from AuthUser:

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

    user = models.OneToOneField('auth.User')

    # personal info
    date_of_birth = models.DateTimeField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True,
                           choices=(('M', 'male'), ('F', 'female')))
    social_security_number = models.CharField(max_length=11, blank=True,
                                              null=True)
    state_id_number = models.CharField(max_length=8, blank=True, null=True)

    competes = models.ManyToManyField('competitions.Competition',
                    through='competitions.CompetitionUserRegistration',
                    blank=True)

    # address information
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    parent_phone_number = models.CharField(max_length=30, blank=True, null=True)
    address = models.ForeignKey('schools.Address', blank=True, null=True)

    # school related info
    school = models.ForeignKey('schools.School', blank=True, null=True)
    school_class = models.CharField(max_length=20, blank=True, null=True)
    classlevel = models.CharField(max_length=2, blank=True, null=True,
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
        return self.user.username + "'s user profile"

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'


class OrganizerProfile(models.Model):
    '''
    Represents an organizer profile.

    Organizer can organize multiple competitions or events.
    '''

    user = models.OneToOneField('auth.User')
    motto = models.CharField(max_length=250, blank=True, null=True)

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

    def __unicode__(self):
        return self.user.username + "'s organizer profile"

    class Meta:
        verbose_name = 'Organizer profile'
        verbose_name_plural = 'Organizer profiles'


@receiver(post_save, sender=User)
def assign_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.save()
