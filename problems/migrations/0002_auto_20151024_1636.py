# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models
import base.storage
import problems.models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersolution',
            name='solution',
            field=base.models.ContentTypeRestrictedFileField(storage=base.storage.OverwriteFileSystemStorage(base_url=b'/protected/', location=b'/home/tbabej/Projects/roots-env/roots/protected/'), upload_to=problems.models.get_solution_path_global, null=True, verbose_name='solution', blank=True),
            preserve_default=True,
        ),
    ]
