# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repository_id', models.CharField(max_length=511)),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=511)),
                ('languages', models.CharField(max_length=511)),
                ('tags', models.CharField(max_length=1023)),
            ],
        ),
    ]
