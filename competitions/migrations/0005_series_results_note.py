# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0004_auto_20151024_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='results_note',
            field=models.CharField(max_length=500, null=True, verbose_name='note in results', blank=True),
            preserve_default=True,
        ),
    ]
