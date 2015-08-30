# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('competitions', '0002_series_problemset'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='site',
            field=models.ForeignKey(blank=True, to='sites.Site', null=True),
            preserve_default=True,
        ),
    ]
