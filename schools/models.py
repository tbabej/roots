from django.db import models
from django.contrib import admin


class Address(models.Model):
    """
    Represents a postal address.
    """

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


class School(models.Model):
    """
    Represents an educational instutition, also known as school, gymnasium,
    lyceum or torture room.
    """

    name = models.CharField(max_length=150)
    address = models.ForeignKey('schools.Address', blank=True)


# Register to the admin site
admin.site.register(Address)
admin.site.register(School)