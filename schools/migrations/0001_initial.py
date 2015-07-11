# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=200, verbose_name='street', blank=True)),
                ('city', models.CharField(max_length=100, verbose_name='city', blank=True)),
                ('postal_number', models.CharField(max_length=10, verbose_name='zip code', blank=True)),
                ('region', models.CharField(max_length=30, verbose_name='region', blank=True)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150, verbose_name='name')),
                ('abbreviation', models.CharField(max_length=20, verbose_name='abbreviation')),
                ('address', models.ForeignKey(verbose_name='address', blank=True, to='schools.Address')),
            ],
            options={
                'verbose_name': 'school',
                'verbose_name_plural': 'schools',
            },
            bases=(models.Model,),
        ),
    ]
