# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Leaflet'
        db.create_table(u'leaflets_leaflet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('competition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['competitions.Competition'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('issue', self.gf('django.db.models.fields.IntegerField')()),
            ('leaflet', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'leaflets', ['Leaflet'])


    def backwards(self, orm):
        # Deleting model 'Leaflet'
        db.delete_table(u'leaflets_leaflet')


    models = {
        u'competitions.competition': {
            'Meta': {'ordering': "['name']", 'object_name': 'Competition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'leaflets.leaflet': {
            'Meta': {'ordering': "['competition', '-year', 'issue']", 'object_name': 'Leaflet'},
            'competition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['competitions.Competition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.IntegerField', [], {}),
            'leaflet': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['leaflets']