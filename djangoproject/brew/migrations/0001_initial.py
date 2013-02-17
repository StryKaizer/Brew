# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brew'
        db.create_table('brew_brew', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('brew', ['Brew'])

        # Adding model 'MashingSchemeItem'
        db.create_table('brew_mashingschemeitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brew', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brew.Brew'])),
            ('minutes', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('degrees', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('brew', ['MashingSchemeItem'])

        # Adding model 'Batch'
        db.create_table('brew_batch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brew', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brew.Brew'])),
            ('brewing_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('mashing_scheme_start', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('brew', ['Batch'])

        # Adding model 'MashingTempLog'
        db.create_table('brew_mashingtemplog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brew.Batch'])),
            ('degrees', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('brew', ['MashingTempLog'])

        # Adding model 'Variable'
        db.create_table('brew_variable', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('brew', ['Variable'])


    def backwards(self, orm):
        # Deleting model 'Brew'
        db.delete_table('brew_brew')

        # Deleting model 'MashingSchemeItem'
        db.delete_table('brew_mashingschemeitem')

        # Deleting model 'Batch'
        db.delete_table('brew_batch')

        # Deleting model 'MashingTempLog'
        db.delete_table('brew_mashingtemplog')

        # Deleting model 'Variable'
        db.delete_table('brew_variable')


    models = {
        'brew.batch': {
            'Meta': {'object_name': 'Batch'},
            'brew': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Brew']"}),
            'brewing_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mashing_scheme_start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'brew.brew': {
            'Meta': {'object_name': 'Brew'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'brew.mashingschemeitem': {
            'Meta': {'object_name': 'MashingSchemeItem'},
            'brew': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Brew']"}),
            'degrees': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'brew.mashingtemplog': {
            'Meta': {'object_name': 'MashingTempLog'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Batch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'degrees': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'brew.variable': {
            'Meta': {'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['brew']