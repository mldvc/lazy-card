# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-09 00:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_reference', '0004_employmenttypes'),
        ('app_id_form', '0003_auto_20171003_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='id_form',
            name='emp_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_reference.EmploymentTypes'),
        ),
    ]