from django.contrib import admin

# Register your models here.
from .models import *

class customer_data_Admin(admin.ModelAdmin):
	list_display=["name","dse","mobile","followup","modified","created"]
admin.site.register(customer_data,customer_data_Admin)

class vehicle_selected_data_Admin(admin.ModelAdmin):
	list_display=["customer","name","model","modified","created"]
admin.site.register(vehicle_selected_data,vehicle_selected_data_Admin)

class followup_data_Admin(admin.ModelAdmin):
	list_display=["customer","followupby","modified","created"]
admin.site.register(followup_data,followup_data_Admin)

class district_data_Admin(admin.ModelAdmin):
	list_display=["name","modified","created"]
admin.site.register(district_data,district_data_Admin)

class town_data_Admin(admin.ModelAdmin):
	list_display=["name","modified","created"]
admin.site.register(town_data,town_data_Admin)

class vehicle_data_Admin(admin.ModelAdmin):
	list_display=["name","modified","created"]
admin.site.register(vehicle_data,vehicle_data_Admin)

class vehicle_model_data_Admin(admin.ModelAdmin):
	list_display=["name","modified","created"]
admin.site.register(vehicle_model_data,vehicle_model_data_Admin)

class financier_data_Admin(admin.ModelAdmin):
	list_display=["name","modified","created"]
admin.site.register(financier_data,financier_data_Admin)

class application_data_Admin(admin.ModelAdmin):
	list_display=["name","modified","created"]
admin.site.register(application_data,application_data_Admin)

class location_data_Admin(admin.ModelAdmin):
	list_display=["name","modified","created"]
admin.site.register(location_data,location_data_Admin)
