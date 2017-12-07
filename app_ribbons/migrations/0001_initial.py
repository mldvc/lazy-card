# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-02 00:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_printers', '0001_initial'),
        ('app_overview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RibbonUsageRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ribbon_number', models.IntegerField(unique=True, verbose_name='Ribbon No.')),
                ('ribbon_use_date', models.DateField(verbose_name='Use Date')),
                ('ribbon_status', models.CharField(choices=[('E', 'Empty'), ('A', 'Active')], max_length=1, verbose_name='Status')),
                ('ribbon_total_printed', models.IntegerField(verbose_name='Total ID Printed')),
                ('ribbon_printer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_printers.Printers', to_field='printer_name')),
                ('ribbon_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_overview.Printer_Ribbon', to_field='ribbon_type')),
            ],
            options={
                'verbose_name': 'Ribbon Usage Record',
                'verbose_name_plural': 'Ribbon Usage Records',
            },
        ),
    ]
