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

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return (
            "street__icontains",
            "city__icontains",
            )

    def __unicode__(self):
        template = u"{street}, {city}, {postal}, {region}"
        return template.format(street=self.street,
                               city=self.city,
                               postal=self.postal_number,
                               region=self.region
                               )

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


class School(models.Model):
    """
    Represents an educational instutition, also known as school, gymnasium,
    lyceum or torture room.
    """

    name = models.CharField(max_length=150,
                            verbose_name=_('name'),
                            unique=True)
    address = models.ForeignKey('schools.Address',
                                blank=True,
                                verbose_name=_('address'))
    abbreviation = models.CharField(max_length=20,
                                    verbose_name=_('abbreviation'))


    def get_num_competitors(self):
        return self.userprofile_set.all().count()
    get_num_competitors.short_description = _("Number of competitors")

    # Define autocomplete fields for grapelli search in admin
    @staticmethod
    def autocomplete_search_fields():
        return (
            "name__incontains",
            "abbreviation__incontains",
            "address__street_icontains",
            "address__city__icontains",
            )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('school')
        verbose_name_plural = _('schools')
