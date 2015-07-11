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
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(max_length=500, verbose_name='heading')),
                ('text', models.CharField(max_length=500, null=True, verbose_name='text', blank=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('added_by', models.ForeignKey(related_name='News_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author')),
                ('competition', models.ForeignKey(verbose_name='competition', to='competitions.Competition')),
                ('modified_by', models.ForeignKey(related_name='News_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
            bases=(models.Model,),
        ),
    ]
