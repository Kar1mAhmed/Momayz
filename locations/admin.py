from django.contrib import admin
from .models import Govern, Area
# Register your models here.
admin.site.register(Govern)


class AreaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Area._meta.fields]
    
admin.site.register(Area, AreaAdmin)
