# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-26 07:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_overview', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='printer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_printers.Printers'),
        ),
    ]