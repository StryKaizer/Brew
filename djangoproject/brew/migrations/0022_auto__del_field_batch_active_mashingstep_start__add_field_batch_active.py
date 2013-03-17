# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Batch.active_mashingstep_start'
        db.delete_column('brew_batch', 'active_mashingstep_start')

        # Adding field 'Batch.active_mashingstep_state_start'
        db.add_column('brew_batch', 'active_mashingstep_state_start',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 3, 17, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Batch.active_mashingstep_start'
        raise RuntimeError("Cannot reverse this migration. 'Batch.active_mashingstep_start' and its values cannot be restored.")
        # Deleting field 'Batch.active_mashingstep_state_start'
        db.delete_column('brew_batch', 'active_mashingstep_state_start')


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
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '3'})
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
            'active_mashing_step_state': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Batch']"}),
            'chart_icon': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'degrees': ('django.db.models.fields.FloatField', [], {}),
            'heat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'brew.variable': {
            'Meta': {'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['brew']