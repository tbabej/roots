# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='problemset',
            field=models.OneToOneField(null=True, blank=True, to='problems.ProblemSet', verbose_name='problem set assigned'),
            preserve_default=True,
        ),
    ]
