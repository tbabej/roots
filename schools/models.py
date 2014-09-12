from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):
    """
    Represents a postal address.
    """

    street = models.CharField(max_length=200,
                              blank=True,
                              verbose_name=_('street'))
    city = models.CharField(max_length=100,
                            blank=True,
                            verbose_name=_('city'))
    postal_number = models.CharField(max_length=10,
                                     blank=True,
                                     verbose_name=_('zip code'))
    region = models.CharField(max_length=30,
                              blank=True,
                              verbose_name=_('region'))

    def __unicode__(self):
        template = u"{street}, {city}, {postal}, {region}"
        return template.format(street=self.street,
                               city=self.city,
                               postal=self.postal_number,
                               region=self.region
                               )


class School(models.Model):
    """
    Represents an educational instutition, also known as school, gymnasium,
    lyceum or torture room.
    """

    name = models.CharField(max_length=150,
                            verbose_name=_('name'))
    address = models.ForeignKey('schools.Address',
                                blank=True,
                                verbose_name=_('address'))

    def __unicode__(self):
        return self.name


# Register to the admin site
admin.site.register(Address)
admin.site.register(School)