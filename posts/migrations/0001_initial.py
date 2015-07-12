# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0008_auto_20150509_1557'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('text', models.TextField(verbose_name='text')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('published', models.BooleanField(default=False, help_text='Post is hidden from non-administrators unless explicitly marked as published here.', verbose_name='published')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('added_by', models.ForeignKey(related_name='Post_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author')),
                ('gallery', models.ForeignKey(blank=True, to='photologue.Gallery', help_text='gallery to be previewed with thepost', null=True, verbose_name='associated gallery')),
                ('modified_by', models.ForeignKey(related_name='Post_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by')),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
            bases=(models.Model,),
        ),
    ]
