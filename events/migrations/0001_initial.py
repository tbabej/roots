# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'], null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('registration_end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'Event_created', null=True, to=orm['auth.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'Event_modified', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding model 'EventUserRegistration'
        db.create_table(u'events_eventuserregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['EventUserRegistration'])

        # Adding unique constraint on 'EventUserRegistration', fields ['event', 'user']
        db.create_unique(u'events_eventuserregistration', ['event_id', 'user_id'])

        # Adding model 'EventOrgRegistration'
        db.create_table(u'events_eventorgregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('organizer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['EventOrgRegistration'])

        # Adding unique constraint on 'EventOrgRegistration', fields ['event', 'organizer']
        db.create_unique(u'events_eventorgregistration', ['event_id', 'organizer_id'])

        # Adding model 'Camp'
        db.create_table(u'events_camp', (
            (u'event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['events.Event'], unique=True, primary_key=True)),
            ('invitation_deadline', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('limit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Season'], null=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['Camp'])

        # Adding model 'CampUserInvitation'
        db.create_table(u'events_campuserinvitation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('camp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Camp'])),
            ('invited_as', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('user_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_accepted_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('org_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'events', ['CampUserInvitation'])

        # Adding unique constraint on 'CampUserInvitation', fields ['user', 'camp']
        db.create_unique(u'events_campuserinvitation', ['user_id', 'camp_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'CampUserInvitation', fields ['user', 'camp']
        db.delete_unique(u'events_campuserinvitation', ['user_id', 'camp_id'])

        # Removing unique constraint on 'EventOrgRegistration', fields ['event', 'organizer']
        db.delete_unique(u'events_eventorgregistration', ['event_id', 'organizer_id'])

        # Removing unique constraint on 'EventUserRegistration', fields ['event', 'user']
        db.delete_unique(u'events_eventuserregistration', ['event_id', 'user_id'])

        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Deleting model 'EventUserRegistration'
        db.delete_table(u'events_eventuserregistration')

        # Deleting model 'EventOrgRegistration'
        db.delete_table(u'events_eventorgregistration')

        # Deleting model 'Camp'
        db.delete_table(u'events_camp')

        # Deleting model 'CampUserInvitation'
        db.delete_table(u'events_campuserinvitation')


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
        u'competitions.season': {
            'Meta': {'ordering': "['competition', 'year', 'number']", 'object_name': 'Season'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Season_created'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'Season_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'sum_method': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.camp': {
            'Meta': {'ordering': "['-start_time', 'end_time']", 'object_name': 'Camp', '_ormbases': [u'events.Event']},
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['events.Event']", 'unique': 'True', 'primary_key': 'True'}),
            'invitation_deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'invited': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['events.CampUserInvitation']", 'symmetrical': 'False'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Season']", 'null': 'True', 'blank': 'True'})
        },
        u'events.campuserinvitation': {
            'Meta': {'ordering': "(u'_order',)", 'unique_together': "(('user', 'camp'),)", 'object_name': 'CampUserInvitation'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'camp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Camp']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited_as': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'org_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'user_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_accepted_timestamp': ('django.db.models.fields.DateTimeField', [], {})
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
        }
    }

    complete_apps = ['events']