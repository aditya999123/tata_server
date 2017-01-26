from __future__ import unicode_literals

from django.db import models

# Create your models here.
# Create your models here.

class KEYS_list(models.Model):
	key=models.CharField(max_length=120,unique=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	def __unicode__(self):
		return str(self.key)

class KEYS_internal(models.Model):
	key=models.ForeignKey(KEYS_list,to_field='key')
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)
	value=models.CharField(max_length=120,blank=True,null=True)

class KEYS_custom(models.Model):
	key=models.ForeignKey(KEYS_list,to_field='key')
	value=models.CharField(max_length=120,blank=True,null=True)
	modified= models.DateTimeField(auto_now=True,auto_now_add=False)
	created= models.DateTimeField(auto_now=False,auto_now_add=True)