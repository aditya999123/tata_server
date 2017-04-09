from __future__ import unicode_literals

from django.db import models

# Create your models here.
class customer_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	mobile=models.CharField(max_length=40,null=True,blank=True)
	address=models.CharField(max_length=200,null=True,blank=True)
	email=models.CharField(max_length=30,null=True,blank=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	def __unicode__(self):
		return self.name

class vehicle_selected_data(models.Model):
	customer=models.ForeignKey(customer_data,null=True)
	name=models.CharField(max_length=20,blank=True,null=True)
	model=models.CharField(max_length=40,null=True,blank=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

class district_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

class town_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

class vehicle_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

class vehicle_model_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

class financier_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

class application_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)

class location_data(models.Model):
	name=models.CharField(max_length=20,blank=True,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
