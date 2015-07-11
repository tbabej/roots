# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import downloads.models
import base.storage
import base.models
from django.conf import settings
import problems.models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leaflets', '0001_initial'),
        ('schools', '0001_initial'),
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgSolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('added_by', models.ForeignKey(related_name='OrgSolution_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author')),
                ('modified_by', models.ForeignKey(related_name='OrgSolution_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by')),
                ('organizer', models.ForeignKey(verbose_name='organizer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'organizer solution',
                'verbose_name_plural': 'organizer solutions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(help_text='The problem itself. Please insert it in a valid TeX formatting.', verbose_name='problem text')),
                ('result', models.TextField(help_text='The result of the problem. For problems that do not have simple results, a hint or short outline of the solution.', null=True, verbose_name='Result / short solution outline', blank=True)),
                ('source', models.CharField(help_text='Source where you found the problem(if not original).', max_length=500, null=True, verbose_name='problem source', blank=True)),
                ('image', models.ImageField(storage=base.storage.OverwriteFileSystemStorage(), upload_to=b'problems/', blank=True, help_text='Image added to the problem text.', null=True, verbose_name='image')),
                ('additional_files', models.FileField(storage=base.storage.OverwriteFileSystemStorage(), upload_to=b'problems/', blank=True, help_text='Additional files stored with the problem (such as editable images).', null=True, verbose_name='additional files')),
                ('rating_votes', models.PositiveIntegerField(default=0, editable=False, blank=True)),
                ('rating_score', models.IntegerField(default=0, editable=False, blank=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('added_by', models.ForeignKey(related_name='Problem_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author')),
            ],
            options={
                'verbose_name': 'problem',
                'verbose_name_plural': 'problems',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProblemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('competition', models.ForeignKey(verbose_name='competition', to='competitions.Competition', help_text='The reference to the competition that uses this category. It makes sense to have categories specific to each competition, since problem types in competitions may differ significantly.')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProblemInSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveSmallIntegerField(verbose_name='position')),
                ('problem', models.ForeignKey(verbose_name='problem', to='problems.Problem')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'problem',
                'verbose_name_plural': 'problems',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'name')),
                ('description', models.CharField(max_length=400, null=True, verbose_name=b'description', blank=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('added_by', models.ForeignKey(related_name='ProblemSet_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author')),
                ('competition', models.ForeignKey(verbose_name='competition', to='competitions.Competition')),
                ('event', models.ForeignKey(verbose_name='event', blank=True, to='events.Event', null=True)),
                ('leaflet', models.ForeignKey(verbose_name='leaflet', blank=True, to='leaflets.Leaflet', null=True)),
                ('modified_by', models.ForeignKey(related_name='ProblemSet_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by')),
                ('problems', sortedm2m.fields.SortedManyToManyField(help_text=None, to='problems.Problem', verbose_name='problems', through='problems.ProblemInSet')),
            ],
            options={
                'verbose_name': 'Problem set',
                'verbose_name_plural': 'Problem sets',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProblemSeverity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('level', models.IntegerField(verbose_name='level')),
                ('competition', models.ForeignKey(verbose_name='competition', to='competitions.Competition', help_text='The reference to the competition that uses this severity. It makes sense to have severities specific to each competition, since organizers might have different ways of sorting the problems regarding their severity.')),
            ],
            options={
                'ordering': ['level'],
                'verbose_name': 'severity',
                'verbose_name_plural': 'severities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSolution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('solution', base.models.ContentTypeRestrictedFileField(storage=base.storage.OverwriteFileSystemStorage(base_url=b'/protected/', location=b'/home/tbabej/Projects/roots-env/roots/protected/'), upload_to=problems.models.get_solution_path_global, null=True, verbose_name='solution')),
                ('corrected_solution', base.models.ContentTypeRestrictedFileField(storage=base.storage.OverwriteFileSystemStorage(base_url=b'/protected/', location=b'/home/tbabej/Projects/roots-env/roots/protected/'), upload_to=problems.models.get_corrected_solution_path_global, null=True, verbose_name='corrected solution', blank=True)),
                ('score', models.IntegerField(null=True, verbose_name='score', blank=True)),
                ('classlevel', models.CharField(blank=True, max_length=2, null=True, verbose_name='class level at the time of submission', choices=[(b'Z2', b'Z2'), (b'Z3', b'Z3'), (b'Z4', b'Z4'), (b'Z5', b'Z5'), (b'Z6', b'Z6'), (b'Z7', b'Z7'), (b'Z8', b'Z8'), (b'Z9', b'Z9'), (b'S1', b'S1'), (b'S2', b'S2'), (b'S3', b'S3'), (b'S4', b'S4')])),
                ('school_class', models.CharField(max_length=20, null=True, verbose_name='school class', blank=True)),
                ('note', models.CharField(max_length=200, null=True, blank=True)),
                ('user_modified_at', models.DateTimeField(auto_now=True, verbose_name='last user modification')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('added_by', models.ForeignKey(related_name='UserSolution_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='author')),
                ('corrected_by', models.ManyToManyField(related_name='usersolutions_corrected_set', verbose_name='corrected by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='UserSolution_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by')),
                ('problem', models.ForeignKey(verbose_name='problem', to='problems.Problem')),
                ('school', models.ForeignKey(verbose_name='school', blank=True, to='schools.School', null=True)),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user solution',
                'verbose_name_plural': 'user solutions',
            },
            bases=(base.models.MediaRemovalMixin, downloads.models.AccessFilePermissionMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='usersolution',
            unique_together=set([('user', 'problem')]),
        ),
        migrations.AlterOrderWithRespectTo(
            name='usersolution',
            order_with_respect_to='problem',
        ),
        migrations.AddField(
            model_name='probleminset',
            name='problemset',
            field=models.ForeignKey(verbose_name='problem set', to='problems.ProblemSet'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='probleminset',
            unique_together=set([('problem', 'problemset')]),
        ),
        migrations.AddField(
            model_name='problem',
            name='category',
            field=models.ForeignKey(verbose_name='category', to='problems.ProblemCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='problem',
            name='competition',
            field=models.ForeignKey(verbose_name='competition', to='competitions.Competition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='problem',
            name='modified_by',
            field=models.ForeignKey(related_name='Problem_modified', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='last modified by'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='problem',
            name='severity',
            field=models.ForeignKey(verbose_name='severity', to='problems.ProblemSeverity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orgsolution',
            name='problem',
            field=models.ForeignKey(verbose_name='problem', to='problems.Problem'),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='orgsolution',
            order_with_respect_to='problem',
        ),
    ]
