# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Competition'
        db.create_table(u'competitions_competition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'competitions', ['Competition'])

        # Adding model 'CompetitionUserRegistration'
        db.create_table(u'competitions_competitionuserregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.UserProfile'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'competitions', ['CompetitionUserRegistration'])

        # Adding model 'CompetitionOrgRegistration'
        db.create_table(u'competitions_competitionorgregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.UserProfile'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'competitions', ['CompetitionOrgRegistration'])

        # Adding model 'Season'
        db.create_table(u'competitions_season', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'competitions', ['Season'])


    def backwards(self, orm):
        # Deleting model 'Competition'
        db.delete_table(u'competitions_competition')

        # Deleting model 'CompetitionUserRegistration'
        db.delete_table(u'competitions_competitionuserregistration')

        # Deleting model 'CompetitionOrgRegistration'
        db.delete_table(u'competitions_competitionorgregistration')

        # Deleting model 'Season'
        db.delete_table(u'competitions_season')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'competitions.competition': {
            'Meta': {'ordering': "['name']", 'object_name': 'Competition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'competitions.competitionorgregistration': {
            'Meta': {'object_name': 'CompetitionOrgRegistration'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.UserProfile']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'competitions.competitionuserregistration': {
            'Meta': {'object_name': 'CompetitionUserRegistration'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.UserProfile']"})
        },
        u'competitions.season': {
            'Meta': {'ordering': "['competition', 'year', 'number']", 'object_name': 'Season'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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