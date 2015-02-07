# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table(u'schools_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('postal_number', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'schools', ['Address'])

        # Adding model 'School'
        db.create_table(u'schools_school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=150)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schools.Address'], blank=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'schools', ['School'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table(u'schools_address')

        # Deleting model 'School'
        db.delete_table(u'schools_school')


    models = {
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

    complete_apps = ['schools']