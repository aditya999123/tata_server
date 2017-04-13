# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-13 02:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_user', '0004_auto_20170413_0743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dsm_data',
            old_name='terget_monthly_dsm',
            new_name='target_monthly_dsm',
        ),
        migrations.AddField(
            model_name='dsm_data',
            name='total_customer_this_month',
            field=models.IntegerField(default=0),
        ),
    ]