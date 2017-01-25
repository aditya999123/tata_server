from django.contrib import admin

# Register your models here.
from .models import *

class KEYS_internal_admin(admin.ModelAdmin):
   list_display=["key","value"]
admin.site.register(KEYS_internal,KEYS_internal_admin)

class KEYS_custom_Admin(admin.ModelAdmin):
   list_display=["key","value"]
admin.site.register(KEYS_custom,KEYS_custom_Admin)

class KEYS_list_Admin(admin.ModelAdmin):
   list_display=["key"]
admin.site.register(KEYS_list,KEYS_list_Admin)
