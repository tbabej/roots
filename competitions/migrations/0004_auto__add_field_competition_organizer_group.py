# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Competition.organizer_group'
        db.add_column(u'competitions_competition', 'organizer_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Competition.organizer_group'
        db.delete_column(u'competitions_competition', 'organizer_group_id')


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
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'competitions_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'competitions_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'organizer_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'null': 'True', 'blank': 'True'})
        },
        u'competitions.competitionorgregistration': {
            'Meta': {'ordering': "['added_at']", 'object_name': 'CompetitionOrgRegistration'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizer registration_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'approved': ('django.db.models.fields.BooleanField', [], {}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizer registration_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.UserProfile']"})
        },
        u'competitions.competitionuserregistration': {
            'Meta': {'ordering': "['added_at']", 'object_name': 'CompetitionUserRegistration'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user registrations_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user registrations_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.UserProfile']"})
        },
        u'competitions.season': {
            'Meta': {'ordering': "['competition', 'year', 'number']", 'object_name': 'Season'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seasons_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seasons_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'competitions.series': {
            'Meta': {'ordering': "['submission_deadline']", 'unique_together': "(('season', 'number'),)", 'object_name': 'Series'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'series_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'series_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'problemset': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['problems.ProblemSet']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Season']"}),
            'submission_deadline': ('django.db.models.fields.DateTimeField', [], {})
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
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
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
        u'problems.problem': {
            'Meta': {'object_name': 'Problem'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'problems_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.ProblemCategory']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'problems_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'severity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['problems.ProblemSeverity']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'problems.problemcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProblemCategory'},
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
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sets_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leaflet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['leaflets.Leaflet']", 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sets_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'problems': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['problems.Problem']", 'through': u"orm['problems.ProblemInSet']", 'symmetrical': 'False'})
        },
        u'problems.problemseverity': {
            'Meta': {'ordering': "['level']", 'object_name': 'ProblemSeverity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'profiles.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.Address']", 'null': 'True', 'blank': 'True'}),
            'classlevel': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'competes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['competitions.Competition']", 'symmetrical': 'False', 'through': u"orm['competitions.CompetitionUserRegistration']", 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.School']", 'null': 'True', 'blank': 'True'}),
            'school_class': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'social_security_number': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'state_id_number': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
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
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['schools.Address']", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['competitions']