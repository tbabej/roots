# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models
import leaflets.models
import base.storage


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaflet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(verbose_name='year')),
                ('issue', models.IntegerField(verbose_name='issue')),
                ('leaflet', models.FileField(upload_to=leaflets.models.get_leaflet_path_global, storage=base.storage.OverwriteFileSystemStorage(), verbose_name='leaflet')),
                ('competition', models.ForeignKey(verbose_name='competition', to='competitions.Competition')),
            ],
            options={
                'ordering': ['competition', '-year', 'issue'],
                'verbose_name': 'leaflet',
                'verbose_name_plural': 'leaflets',
            },
            bases=(base.models.MediaRemovalMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='leaflet',
            unique_together=set([('competition', 'year', 'issue')]),
        ),
    ]
