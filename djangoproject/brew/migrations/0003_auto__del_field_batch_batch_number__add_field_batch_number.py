# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Batch.batch_number'
        db.delete_column('brew_batch', 'batch_number')

        # Adding field 'Batch.number'
        db.add_column('brew_batch', 'number',
                      self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Batch.batch_number'
        raise RuntimeError("Cannot reverse this migration. 'Batch.batch_number' and its values cannot be restored.")
        # Deleting field 'Batch.number'
        db.delete_column('brew_batch', 'number')


    models = {
        'brew.batch': {
            'Meta': {'object_name': 'Batch'},
            'brew': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Brew']"}),
            'brewing_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mashing_scheme_start': ('django.db.models.fields.DateTimeField', [], {}),
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
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