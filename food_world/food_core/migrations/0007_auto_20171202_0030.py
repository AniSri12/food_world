# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-02 00:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_core', '0006_auto_20171030_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='authenticator',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='food_core.Authenticator'),
        ),
    ]
