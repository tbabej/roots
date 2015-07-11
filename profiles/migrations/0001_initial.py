# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schools', '0001_initial'),
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('motto', models.CharField(max_length=250, null=True, verbose_name='motto', blank=True)),
                ('user', models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'organizer profile',
                'verbose_name_plural': 'organizer profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField(null=True, verbose_name='date of birth', blank=True)),
                ('sex', models.CharField(blank=True, max_length=1, null=True, verbose_name='sex', choices=[(b'M', 'male'), (b'F', 'female')])),
                ('phone_number', models.CharField(max_length=30, null=True, verbose_name='phone number', blank=True)),
                ('parent_phone_number', models.CharField(max_length=30, null=True, verbose_name='parent phone number', blank=True)),
                ('school_class', models.CharField(max_length=20, null=True, verbose_name='school class', blank=True)),
                ('classlevel', models.CharField(blank=True, max_length=2, null=True, verbose_name='class level', choices=[(b'Z2', b'Z2'), (b'Z3', b'Z3'), (b'Z4', b'Z4'), (b'Z5', b'Z5'), (b'Z6', b'Z6'), (b'Z7', b'Z7'), (b'Z8', b'Z8'), (b'Z9', b'Z9'), (b'S1', b'S1'), (b'S2', b'S2'), (b'S3', b'S3'), (b'S4', b'S4')])),
                ('address', models.ForeignKey(verbose_name='address', blank=True, to='schools.Address', null=True)),
                ('school', models.ForeignKey(verbose_name='school', blank=True, to='schools.School', null=True)),
                ('user', models.OneToOneField(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSeasonRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('school_class', models.CharField(max_length=20, null=True, verbose_name='school class', blank=True)),
                ('classlevel', models.CharField(blank=True, max_length=2, null=True, verbose_name='class level', choices=[(b'Z2', b'Z2'), (b'Z3', b'Z3'), (b'Z4', b'Z4'), (b'Z5', b'Z5'), (b'Z6', b'Z6'), (b'Z7', b'Z7'), (b'Z8', b'Z8'), (b'Z9', b'Z9'), (b'S1', b'S1'), (b'S2', b'S2'), (b'S3', b'S3'), (b'S4', b'S4')])),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('added_by', models.ForeignKey(related_name='UserSeasonRegistration_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author')),
                ('modified_by', models.ForeignKey(related_name='UserSeasonRegistration_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by')),
                ('school', models.ForeignKey(verbose_name='school', blank=True, to='schools.School', null=True)),
                ('season', models.ForeignKey(verbose_name='season', to='competitions.Season')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user season registration',
                'verbose_name_plural': 'user season registrations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='userseasonregistration',
            unique_together=set([('season', 'user')]),
        ),
    ]
