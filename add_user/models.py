from __future__ import unicode_literals

from django.db import models

# Create your models here.
class user_level(models.Model):
	user_level=models.IntegerField(default=0)
	name=models.CharField(max_length=20,blank=False,null=False)

class user_data(models.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=20,blank=False,null=False)
	mobile=models.CharField(max_length=12,blank=False,null=False)
	fcm=models.CharField(max_length=400,blank=False,null=False)

class tsm_data(models.Model):
	user_id=models.ForeignKey(user_data,to_field='id')
	active=models.BooleanField(default=True)

class dsm_data(models.Model):
	user_id=models.ForeignKey(user_data,to_field='id')
	active=models.BooleanField(default=True)

class dse_data(models.Model):
	user_id=models.ForeignKey(user_data,to_field='id')
	active=models.BooleanField(default=True)
