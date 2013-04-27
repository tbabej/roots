from django.db import models
from django.contrib import admin


class Leaflet(models.Model):
    competition = models.ForeignKey('competitions.Competition')
    year = models.IntegerField()

    def __unicode__(self):
        return u"Leaflet for " + self.competition.__unicode__()

# Register to the admin site
admin.site.register(Leaflet)