# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-25 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dse_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='dsm_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='tsm_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, null=True)),
                ('user_name', models.CharField(max_length=20)),
                ('password', models.CharField(default=b'd8022f2060ad6efd297ab73dcc5355c9b214054b0d1776a136a669d26a7d3b14f73aa0d0ebff19ee333368f0164b6419a96da49e3e481753e7e96b716bdccb6f', max_length=1200)),
                ('fcm', models.CharField(blank=True, max_length=400, null=True)),
                ('designation', models.CharField(choices=[('None', 'None'), ('DSE', 'DSE'), ('DSM', 'DSM'), ('TSM', 'TSM')], default='None', max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='tsm_data',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_user.user_data'),
        ),
        migrations.AddField(
            model_name='dsm_data',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_user.user_data'),
        ),
        migrations.AddField(
            model_name='dse_data',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='add_user.user_data'),
        ),
    ]
