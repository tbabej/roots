# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import competitions.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='competition name')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'competition',
                'verbose_name_plural': 'competitions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompetitionOrgRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField(verbose_name='registration approved')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
            ],
            options={
                'ordering': ['added_at'],
                'verbose_name': 'organizer registration',
                'verbose_name_plural': 'organizer registration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompetitionUserRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
            ],
            options={
                'ordering': ['added_at'],
                'verbose_name': 'user registration',
                'verbose_name_plural': 'user registrations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(verbose_name='year')),
                ('number', models.IntegerField(verbose_name='number')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('join_deadline', models.DateTimeField(null=True, verbose_name='join deadline', blank=True)),
                ('start', models.DateTimeField(verbose_name='season start')),
                ('end', models.DateTimeField(verbose_name='season end')),
                ('sum_method', models.CharField(blank=True, max_length=50, null=True, help_text='Method that is used to compute the sum of the season', choices=[(None, b'Simple sum')])),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
            ],
            options={
                'ordering': ['competition', 'year', 'number'],
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
            },
            bases=(models.Model, competitions.models.SeasonSeriesBaseMixin),
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('number', models.PositiveSmallIntegerField(verbose_name='number')),
                ('submission_deadline', models.DateTimeField(verbose_name='series submission deadline')),
                ('is_active', models.BooleanField(default=False, verbose_name='is series active')),
                ('sum_method', models.CharField(choices=[(None, b'Simple sum')], max_length=50, blank=True, help_text='Method that is used to compute the sum of the series', null=True, verbose_name='total method')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('added_by', models.ForeignKey(related_name='Series_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author')),
                ('modified_by', models.ForeignKey(related_name='Series_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by')),
            ],
            options={
                'ordering': ['submission_deadline'],
                'verbose_name': 'Series',
                'verbose_name_plural': 'Series',
            },
            bases=(models.Model, competitions.models.SeasonSeriesBaseMixin),
        ),
    ]
