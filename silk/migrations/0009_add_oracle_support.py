# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-01-10 14:14
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.backends.utils import truncate_name

import silk.storage


def create_autoinc(table_name, column_name):
    def autoinc(apps, schema_editor):
        autoinc_sql = schema_editor.connection.ops.autoinc_sql(table_name, column_name)
        if autoinc_sql:
            schema_editor.deferred_sql.extend(autoinc_sql)

    return autoinc


def remove_autoinc(table_name, column_name):
    def autoinc(apps, schema_editor):
        def _get_trigger_name(table):
            name_length = schema_editor.connection.ops.max_name_length() - 3
            return schema_editor.connection.ops.quote_name('%s_TR' % truncate_name(table, name_length).upper())

        seq_sql = schema_editor.connection.ops.drop_sequence_sql(table_name)
        if seq_sql:
            schema_editor.execute(seq_sql)
            schema_editor.execute('DROP TRIGGER %s;' % _get_trigger_name(table_name))

    return autoinc


class Migration(migrations.Migration):

    dependencies = [
        ('silk', '0008_sqlquery_analysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='request'
        ),
        migrations.RemoveField(
            model_name='sqlquery',
            name='request'
        ),
        migrations.RemoveField(
            model_name='profile',
            name='request'
        ),

        migrations.RemoveField(
            model_name='request',
            name='id'
        ),
        migrations.RemoveField(
            model_name='response',
            name='id'
        ),

        migrations.AddField(
            model_name='request',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='response',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),

        migrations.AddField(
            model_name='response',
            name='request',
            field=models.OneToOneField(to='silk.Request', related_name='response', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='sqlquery',
            name='request',
            field=models.ForeignKey(to='silk.Request', blank=True, null=True, related_name='queries', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='profile',
            name='request',
            field=models.ForeignKey(to='silk.Request', blank=True, null=True, on_delete=models.CASCADE),
        ),

        migrations.RunPython(create_autoinc('silk_request', 'id'), remove_autoinc('silk_request', 'id')),
        migrations.RunPython(create_autoinc('silk_response', 'id'), remove_autoinc('silk_response', 'id')),
        migrations.AlterField(
            model_name='request',
            name='prof_file',
            field=models.FileField(
                default='',
                max_length=300,
                null=True,
                blank=True,
                storage=silk.storage.ProfilerResultStorage(),
            ),
        ),
    ]
