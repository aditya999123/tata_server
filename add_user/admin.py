from django.contrib import admin
from .models import *
# Register your models here.
# class user_level_Admin(admin.ModelAdmin):
#     list_display=["user_level","name"]
# admin.site.register(user_level,user_level_Admin)

class user_data_Admin(admin.ModelAdmin):
	list_display=["name","active","designation","fcm","created","modified"]
	fields=["name","user_name","designation","fcm"]
	#readonly_fields = ['password']
admin.site.register(user_data,user_data_Admin)

class tsm_data_Admin(admin.ModelAdmin):
    list_display=["user_id","created","modified"]
admin.site.register(tsm_data,tsm_data_Admin)

class dsm_data_Admin(admin.ModelAdmin):
    list_display=["user_id","created","modified"]
admin.site.register(dsm_data,dsm_data_Admin)

class dse_data_Admin(admin.ModelAdmin):
    list_display=["user_id","created","modified"]
admin.site.register(dse_data,dse_data_Admin)
