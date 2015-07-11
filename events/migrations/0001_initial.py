# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampUserInvitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invited_as', models.CharField(max_length=3, verbose_name='invited as', choices=[(b'REG', b'regular'), (b'SUB', b'substitute')])),
                ('order', models.IntegerField(verbose_name='order')),
                ('user_accepted', models.BooleanField(default=False, verbose_name='accepted by user')),
                ('user_accepted_timestamp', models.DateTimeField(verbose_name='user accepted timestamp')),
                ('org_accepted', models.BooleanField(default=False, verbose_name='accepted by organizers')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
            ],
            options={
                'verbose_name': 'camp invitation',
                'verbose_name_plural': 'camp invitations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='event name')),
                ('location', models.CharField(max_length=100, verbose_name='event location')),
                ('description', models.CharField(max_length=500, verbose_name='description')),
                ('start_time', models.DateTimeField(verbose_name='start time')),
                ('end_time', models.DateTimeField(verbose_name='end time')),
                ('registration_end_time', models.DateTimeField(null=True, verbose_name='registration end time', blank=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
            ],
            options={
                'ordering': ['-start_time', 'end_time'],
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='events.Event')),
                ('invitation_deadline', models.DateTimeField(null=True, verbose_name='invitation deadline', blank=True)),
                ('limit', models.IntegerField(null=True, verbose_name='participant limit', blank=True)),
            ],
            options={
                'verbose_name': 'camp',
                'verbose_name_plural': 'camps',
            },
            bases=('events.event',),
        ),
        migrations.CreateModel(
            name='EventOrgRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('event', models.ForeignKey(verbose_name='event', to='events.Event')),
                ('organizer', models.ForeignKey(verbose_name='organizer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'organizer registration',
                'verbose_name_plural': 'organizer registrations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventUserRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('event', models.ForeignKey(verbose_name='event', to='events.Event')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user registration',
                'verbose_name_plural': 'user registrations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventuserregistration',
            unique_together=set([('event', 'user')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='eventuserregistration',
            order_with_respect_to='event',
        ),
        migrations.AlterUniqueTogether(
            name='eventorgregistration',
            unique_together=set([('event', 'organizer')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='eventorgregistration',
            order_with_respect_to='event',
        ),
        migrations.AddField(
            model_name='event',
            name='added_by',
            field=models.ForeignKey(related_name='Event_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='competition',
            field=models.ForeignKey(verbose_name='competition', blank=True, to='competitions.Competition', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='modified_by',
            field=models.ForeignKey(related_name='Event_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='registered_org',
            field=models.ManyToManyField(related_name='organized_event_set', verbose_name='registered organizer', through='events.EventOrgRegistration', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='registered_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='registered user', through='events.EventUserRegistration'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campuserinvitation',
            name='camp',
            field=models.ForeignKey(verbose_name='camp', to='events.Camp'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campuserinvitation',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='campuserinvitation',
            unique_together=set([('user', 'camp')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='campuserinvitation',
            order_with_respect_to='camp',
        ),
        migrations.AddField(
            model_name='camp',
            name='invited',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='invited users', through='events.CampUserInvitation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='camp',
            name='season',
            field=models.ForeignKey(verbose_name='event for season', blank=True, to='competitions.Season', null=True),
            preserve_default=True,
        ),
    ]
