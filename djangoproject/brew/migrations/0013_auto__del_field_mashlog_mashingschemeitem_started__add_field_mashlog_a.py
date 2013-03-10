# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MashLog.mashingschemeitem_started'
        db.delete_column('brew_mashlog', 'mashingschemeitem_started_id')

        # Adding field 'MashLog.active_mashing_scheme_item'
        db.add_column('brew_mashlog', 'active_mashing_scheme_item',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['brew.MashingSchemeItem']),
                      keep_default=False)

        # Adding field 'MashLog.status'
        db.add_column('brew_mashlog', 'status',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'MashLog.mashingschemeitem_started'
        db.add_column('brew_mashlog', 'mashingschemeitem_started',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['brew.MashingSchemeItem'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'MashLog.active_mashing_scheme_item'
        db.delete_column('brew_mashlog', 'active_mashing_scheme_item_id')

        # Deleting field 'MashLog.status'
        db.delete_column('brew_mashlog', 'status')


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
            'active_mashing_scheme_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingSchemeItem']"}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.Batch']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'degrees': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'brew.variable': {
            'Meta': {'object_name': 'Variable'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['brew']