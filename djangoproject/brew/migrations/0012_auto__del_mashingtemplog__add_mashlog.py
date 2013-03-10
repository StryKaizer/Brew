# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MashingTempLog'
        db.delete_table('brew_mashingtemplog')

        # Adding model 'MashLog'
        db.create_table('brew_mashlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brew.Batch'])),
            ('degrees', self.gf('django.db.models.fields.FloatField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('mashingschemeitem_started', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['brew.MashingSchemeItem'], null=True, blank=True)),
        ))
        db.send_create_signal('brew', ['MashLog'])


    def backwards(self, orm):
        # Adding model 'MashingTempLog'
        db.create_table('brew_mashingtemplog', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brew.Batch'])),
            ('degrees', self.gf('django.db.models.fields.FloatField')()),
            ('mashingschemeitem_started', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['brew.MashingSchemeItem'], null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('brew', ['MashingTempLog'])

        # Deleting model 'MashLog'
        db.delete_table('brew_mashlog')


    models = {
        'brew.batch': {
            'Meta': {'object_name': 'Batch'},
            'brewing_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mashing_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingScheme']"}),
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
        },
        'brew.mashingscheme': {
            'Meta': {'object_name': 'MashingScheme'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'brew.mashingschemeitem': {
            'Meta': {'object_name': 'MashingSchemeItem'},
            'degrees': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mashing_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingScheme']"}),
            'minutes': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'brew.mashlog': {
            'Meta': {'object_name': 'MashLog'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Batch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'degrees': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mashingschemeitem_started': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['brew.MashingSchemeItem']", 'null': 'True', 'blank': 'True'})
        },
        'brew.variable': {
            'Meta': {'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['brew']