# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Batch.temperature'
        db.add_column('brew_batch', 'temperature',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Deleting field 'MashLog.degrees'
        db.delete_column('brew_mashlog', 'degrees')

        # Adding field 'MashLog.temperature'
        db.add_column('brew_mashlog', 'temperature',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Batch.temperature'
        db.delete_column('brew_batch', 'temperature')


        # User chose to not deal with backwards NULL issues for 'MashLog.degrees'
        raise RuntimeError("Cannot reverse this migration. 'MashLog.degrees' and its values cannot be restored.")
        # Deleting field 'MashLog.temperature'
        db.delete_column('brew_mashlog', 'temperature')


    models = {
        'brew.batch': {
            'Meta': {'object_name': 'Batch'},
            'active_mashingstep': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingStep']"}),
            'active_mashingstep_approach_direction': ('django.db.models.fields.CharField', [], {'default': "'tbd'", 'max_length': '10'}),
            'active_mashingstep_state': ('django.db.models.fields.CharField', [], {'default': "'approach'", 'max_length': '10'}),
            'active_mashingstep_state_start': ('django.db.models.fields.DateTimeField', [], {}),
            'brewing_date': ('django.db.models.fields.DateTimeField', [], {}),
            'cool': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mashing_process_is_running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mashing_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingScheme']"}),
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'temperature': ('django.db.models.fields.FloatField', [], {})
        },
        'brew.mashingscheme': {
            'Meta': {'object_name': 'MashingScheme'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'brew.mashingstep': {
            'Meta': {'ordering': "['position']", 'object_name': 'MashingStep'},
            'degrees': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mashing_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingScheme']"}),
            'minutes': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'brew.mashlog': {
            'Meta': {'object_name': 'MashLog'},
            'active_mashing_step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingStep']"}),
            'active_mashing_step_state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Batch']"}),
            'chart_icon': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'heat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temperature': ('django.db.models.fields.FloatField', [], {})
        },
        'brew.variable': {
            'Meta': {'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['brew']