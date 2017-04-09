from __future__ import unicode_literals

from django.db import models
import hashlib
# Create your models here.
#class user_level(models.Model):
#	user_level=models.IntegerField(default=0)
#	name=models.CharField(max_length=20,blank=False,null=False)

DEG_CHOICES = (
	('-1', 'None'),
        ('2', 'DSE'),
        ('1', 'DSM'),
        ('0', 'TSM'))

class user_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	user_name=models.CharField(max_length=20,blank=False,null=False)
	password=models.CharField(max_length=1200,blank=False,null=False,default=hashlib.sha512('abcd').hexdigest().lower())
	fcm=models.CharField(max_length=400,null=True,blank=True)
	designation=models.CharField(max_length=100,choices=DEG_CHOICES,null=False)
	mobile=models.CharField(max_length=40,null=True,blank=True)
	address=models.CharField(max_length=200,null=True,blank=True)
	profile=models.CharField(max_length=400,null=True,blank=True)
	email=models.CharField(max_length=30,null=True,blank=True)
	image=models.ImageField(upload_to='users/',default="/media/users/default.png")
	active=models.BooleanField(default=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	first_time_user=models.BooleanField(default=True)
	def __unicode__(self):
		return self.user_name

class dealer_data(models.Model):
	name=models.CharField(max_length=40,null=True,blank=True)
	location=models.CharField(max_length=400,null=True,blank=True)
	description=models.CharField(max_length=400,null=True,blank=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	def __unicode__(self):
		return self.name

class tsm_data(models.Model):
	user_id=models.ForeignKey(user_data,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	def __unicode__(self):
		return self.user_id.user_name

class dsm_data(models.Model):
	user_id=models.ForeignKey(user_data,null=True)
	tsm=models.ForeignKey(tsm_data,null=True)
	dealer=models.ForeignKey(dealer_data,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	def __unicode__(self):
		return self.user_id.user_name

class dse_data(models.Model):
	user_id=models.ForeignKey(user_data,null=True)
	dsm=models.ForeignKey(dsm_data,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

