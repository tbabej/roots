# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0003_competition_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='problemset',
            field=models.OneToOneField(verbose_name='problem set assigned', to='problems.ProblemSet'),
            preserve_default=True,
        ),
    ]
