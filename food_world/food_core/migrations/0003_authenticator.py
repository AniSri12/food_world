# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-26 03:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_core', '0002_auto_20171026_0302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
