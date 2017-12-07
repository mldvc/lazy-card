# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-24 04:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_reference', '0002_auto_20170824_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_name', models.CharField(max_length=200, verbose_name='Code Name')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('id_type', models.ManyToManyField(blank=True, to='app_reference.IDTypes')),
            ],
            options={
                'verbose_name': 'Form Field',
                'verbose_name_plural': 'Form Fields',
            },
        ),
        migrations.CreateModel(
            name='ID_Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='Name')),
                ('blood_type', models.CharField(default='N/A', max_length=10, verbose_name='Blood Type')),
                ('birth_day', models.DateField(verbose_name='Date of Birth')),
                ('contact_num', models.CharField(default='N/A', max_length=100, verbose_name='Contact Number')),
                ('ptn', models.CharField(max_length=100, verbose_name='PTN Incase of Emergency')),
                ('ptn_cnum', models.CharField(max_length=100, verbose_name='PTN Contact Number')),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('position', models.CharField(max_length=100, null=True, verbose_name='Position')),
                ('tin', models.CharField(default='N/A', max_length=200, verbose_name='TIN No.')),
                ('sss', models.CharField(default='N/A', max_length=200, verbose_name='SSS No.')),
                ('id_number', models.CharField(max_length=100, verbose_name='ID No.')),
                ('validity', models.CharField(max_length=100, null=True, verbose_name='Validity')),
                ('alu_validity', models.CharField(max_length=100, null=True, verbose_name='Alumni ID Validity')),
                ('add_date', models.DateField(verbose_name='Add Date')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_reference.Courses')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_reference.Departments')),
                ('id_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_reference.IDTypes')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_reference.Levels')),
                ('strand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_reference.Strands')),
            ],
            options={
                'verbose_name': 'ID Forms',
                'verbose_name_plural': 'ID Forms',
            },
        ),
    ]
