from __future__ import unicode_literals

from django.db import models
import hashlib
# Create your models here.
#class user_level(models.Model):
#	user_level=models.IntegerField(default=0)
#	name=models.CharField(max_length=20,blank=False,null=False)

DEG_CHOICES = (
	(4, 'None'),
        (0, 'DSE'),
        (1, 'DSM'),
        (2, 'TSM'))

class user_data(models.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=20,blank=True,null=True)
	user_name=models.CharField(max_length=20,blank=False,null=False)
	password=models.CharField(max_length=1200,blank=False,null=False,default=hashlib.sha512('abcd').hexdigest().lower())
	fcm=models.CharField(max_length=400,null=True,blank=True)
	designation=models.IntegerField(choices=DEG_CHOICES)
	mobile=models.CharField(max_length=12,null=True,blank=True)
	address=models.CharField(max_length=200,null=True,blank=True)
	profile=models.CharField(max_length=400,null=True,blank=True)
	email=models.CharField(max_length=30,null=True,blank=True)
	image=models.ImageField(upload_to='users/',default="/media/users/default.png")
	active=models.BooleanField(default=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

	def __unicode__(self):
		return str(self.user_name)


class tsm_data(models.Model):
	user_id=models.ForeignKey(user_data,to_field='id')
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	#active=models.BooleanField(default=True)
	def __unicode__(self):
		return str(self.user_id)
	#user_id = user_data.objects.filter(designation='None')

class dsm_data(models.Model):
	user_id=models.ForeignKey(user_data,to_field='id')
	tsm=models.ForeignKey(tsm_data,to_field='id')
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	#active=models.BooleanField(default=True)
	def __unicode__(self):
		return str(self.user_id)

class dse_data(models.Model):
	user_id=models.ForeignKey(user_data,to_field='id')
	dsm=models.ForeignKey(dsm_data,to_field='id')
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	#active=models.BooleanField(default=True)
