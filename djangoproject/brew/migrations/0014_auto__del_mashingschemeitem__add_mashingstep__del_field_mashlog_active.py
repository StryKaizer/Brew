# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MashingSchemeItem'
        db.delete_table('brew_mashingschemeitem')

        # Adding model 'MashingStep'
        db.create_table('brew_mashingstep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mashing_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brew.MashingScheme'])),
            ('minutes', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('degrees', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('brew', ['MashingStep'])

        # Deleting field 'MashLog.active_mashing_scheme_item'
        db.delete_column('brew_mashlog', 'active_mashing_scheme_item_id')

        # Adding field 'MashLog.active_mashing_step'
        db.add_column('brew_mashlog', 'active_mashing_step',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['brew.MashingStep']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'MashingSchemeItem'
        db.create_table('brew_mashingschemeitem', (
            ('minutes', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('mashing_scheme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['brew.MashingScheme'])),
            ('degrees', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('brew', ['MashingSchemeItem'])

        # Deleting model 'MashingStep'
        db.delete_table('brew_mashingstep')


        # User chose to not deal with backwards NULL issues for 'MashLog.active_mashing_scheme_item'
        raise RuntimeError("Cannot reverse this migration. 'MashLog.active_mashing_scheme_item' and its values cannot be restored.")
        # Deleting field 'MashLog.active_mashing_step'
        db.delete_column('brew_mashlog', 'active_mashing_step_id')


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
        'brew.mashingstep': {
            'Meta': {'object_name': 'MashingStep'},
            'degrees': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mashing_scheme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingScheme']"}),
            'minutes': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'brew.mashlog': {
            'Meta': {'object_name': 'MashLog'},
            'active_mashing_step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['brew.MashingStep']"}),
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