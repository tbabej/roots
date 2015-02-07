# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserSolution'
        db.create_table(u'problems_usersolution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['problems.Problem'])),
            ('solution', self.gf('base.models.ContentTypeRestrictedFileField')(max_length=100, null=True)),
            ('corrected_solution', self.gf('base.models.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('classlevel', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.School'], null=True, blank=True)),
            ('school_class', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('user_modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'UserSolution_created', null=True, to=orm['auth.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'UserSolution_modified', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'problems', ['UserSolution'])

        # Adding unique constraint on 'UserSolution', fields ['user', 'problem']
        db.create_unique(u'problems_usersolution', ['user_id', 'problem_id'])

        # Adding M2M table for field corrected_by on 'UserSolution'
        m2m_table_name = db.shorten_name(u'problems_usersolution_corrected_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usersolution', models.ForeignKey(orm[u'problems.usersolution'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['usersolution_id', 'user_id'])

        # Adding model 'OrgSolution'
        db.create_table(u'problems_orgsolution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['problems.Problem'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'OrgSolution_created', null=True, to=orm['auth.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'OrgSolution_modified', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'problems', ['OrgSolution'])

        # Adding model 'Problem'
        db.create_table(u'problems_problem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('severity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['problems.ProblemSeverity'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['problems.ProblemCategory'])),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('additional_files', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'Problem_created', null=True, to=orm['auth.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'Problem_modified', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'problems', ['Problem'])

        # Adding model 'ProblemInSet'
        db.create_table(u'problems_probleminset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['problems.Problem'])),
            ('problemset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['problems.ProblemSet'])),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'problems', ['ProblemInSet'])

        # Adding unique constraint on 'ProblemInSet', fields ['problem', 'problemset']
        db.create_unique(u'problems_probleminset', ['problem_id', 'problemset_id'])

        # Adding model 'ProblemSet'
        db.create_table(u'problems_problemset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('leaflet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['leaflets.Leaflet'], null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'], null=True, blank=True)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'ProblemSet_created', null=True, to=orm['auth.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'ProblemSet_modified', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'problems', ['ProblemSet'])

        # Adding model 'ProblemCategory'
        db.create_table(u'problems_problemcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
        ))
        db.send_create_signal(u'problems', ['ProblemCategory'])

        # Adding model 'ProblemSeverity'
        db.create_table(u'problems_problemseverity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
        ))
        db.send_create_signal(u'problems', ['ProblemSeverity'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProblemInSet', fields ['problem', 'problemset']
        db.delete_unique(u'problems_probleminset', ['problem_id', 'problemset_id'])

        # Removing unique constraint on 'UserSolution', fields ['user', 'problem']
        db.delete_unique(u'problems_usersolution', ['user_id', 'problem_id'])

        # Deleting model 'UserSolution'
        db.delete_table(u'problems_usersolution')

        # Removing M2M table for field corrected_by on 'UserSolution'
        db.delete_table(db.shorten_name(u'problems_usersolution_corrected_by'))

        # Deleting model 'OrgSolution'
        db.delete_table(u'problems_orgsolution')

        # Deleting model 'Problem'
        db.delete_table(u'problems_problem')

        # Deleting model 'ProblemInSet'
        db.delete_table(u'problems_probleminset')

        # Deleting model 'ProblemSet'
        db.delete_table(u'problems_problemset')

        # Deleting model 'ProblemCategory'
        db.delete_table(u'problems_problemcategory')

        # Deleting model 'ProblemSeverity'
        db.delete_table(u'problems_problemseverity')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'competitions.competition': {
            'Meta': {'ordering': "['name']", 'object_name': 'Competition'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Competition_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Competition_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'organizer_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.event': {
            'Meta': {'ordering': "['-start_time', 'end_time']", 'object_name': 'Event'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Event_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Event_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'registered_org': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'organized_event_set'", 'symmetrical': 'False', 'through': u"orm['events.EventOrgRegistration']", 'to': u"orm['auth.User']"}),
            'registered_user': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['events.EventUserRegistration']", 'symmetrical': 'False'}),
            'registration_end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'events.eventorgregistration': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('event', 'organizer'),)", 'object_name': 'EventOrgRegistration'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'events.eventuserregistration': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('event', 'user'),)", 'object_name': 'EventUserRegistration'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'leaflets.leaflet': {
            'Meta': {'ordering': "['competition', '-year', 'issue']", 'unique_together': "(('competition', 'year', 'issue'),)", 'object_name': 'Leaflet'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.IntegerField', [], {}),
            'leaflet': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'problems.orgsolution': {
            'Meta': {'ordering': "(u'_order',)", 'object_name': 'OrgSolution'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'OrgSolution_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'OrgSolution_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.Problem']"})
        },
        u'problems.problem': {
            'Meta': {'object_name': 'Problem'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Problem_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'additional_files': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.ProblemCategory']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Problem_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'severity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.ProblemSeverity']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'problems.problemcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProblemCategory'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'problems.probleminset': {
            'Meta': {'ordering': "['position']", 'unique_together': "(['problem', 'problemset'],)", 'object_name': 'ProblemInSet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.Problem']"}),
            'problemset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.ProblemSet']"})
        },
        u'problems.problemset': {
            'Meta': {'object_name': 'ProblemSet'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'ProblemSet_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leaflet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leaflets.Leaflet']", 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'ProblemSet_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'problems': ('sortedm2m.fields.SortedManyToManyField', [], {'to': u"orm['problems.Problem']", 'through': u"orm['problems.ProblemInSet']", 'symmetrical': 'False'})
        },
        u'problems.problemseverity': {
            'Meta': {'ordering': "['level']", 'object_name': 'ProblemSeverity'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'problems.usersolution': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(['user', 'problem'],)", 'object_name': 'UserSolution'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'UserSolution_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'classlevel': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'corrected_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'usersolutions_corrected_set'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'corrected_solution': ('base.models.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'UserSolution_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.Problem']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.School']", 'null': 'True', 'blank': 'True'}),
            'school_class': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'solution': ('base.models.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'user_modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'schools.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'schools.school': {
            'Meta': {'object_name': 'School'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.Address']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        }
    }

    complete_apps = ['problems']