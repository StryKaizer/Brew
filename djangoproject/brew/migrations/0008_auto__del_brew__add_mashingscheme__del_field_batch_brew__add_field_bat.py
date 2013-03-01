# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Brew'
        db.delete_table('brew_brew')

        # Adding model 'MashingScheme'
        db.create_table('brew_mashingscheme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('brew', ['MashingScheme'])

        # Deleting field 'Batch.brew'
        db.delete_column('brew_batch', 'brew_id')

        # Adding field 'Batch.mashing_scheme'
        db.add_column('brew_batch', 'mashing_scheme',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['brew.MashingScheme']),
                      keep_default=False)

        # Deleting field 'MashingSchemeItem.brew'
        db.delete_column('brew_mashingschemeitem', 'brew_id')

        # Adding field 'MashingSchemeItem.mashing_scheme'
        db.add_column('brew_mashingschemeitem', 'mashing_scheme',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['brew.MashingScheme']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Brew'
        db.create_table('brew_brew', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('brew', ['Brew'])

        # Deleting model 'MashingScheme'
        db.delete_table('brew_mashingscheme')


        # User chose to not deal with backwards NULL issues for 'Batch.brew'
        raise RuntimeError("Cannot reverse this migration. 'Batch.brew' and its values cannot be restored.")
        # Deleting field 'Batch.mashing_scheme'
        db.delete_column('brew_batch', 'mashing_scheme_id')


        # User chose to not deal with backwards NULL issues for 'MashingSchemeItem.brew'
        raise RuntimeError("Cannot reverse this migration. 'MashingSchemeItem.brew' and its values cannot be restored.")
        # Deleting field 'MashingSchemeItem.mashing_scheme'
        db.delete_column('brew_mashingschemeitem', 'mashing_scheme_id')


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
        'brew.mashingtemplog': {
            'Meta': {'object_name': 'MashingTempLog'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Batch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'degrees': ('django.db.models.fields.FloatField', [], {}),
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