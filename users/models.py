from django.db import models
from django.contrib import admin


# User-related models
class User(models.Model):
    login = models.CharField(max_length=50)
    competes = models.ManyToManyField('competitions.Competition',
                    through='competitions.CompetitionUserRegistration')
    solved = models.ManyToManyField('problems.Problem')

    def __unicode__(self):
        return self.login


class Organizer(User):
    motto = models.CharField(max_length=50)

# Register to the admin site
admin.site.register(User)
admin.site.register(Organizer)
