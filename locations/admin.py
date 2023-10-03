from django.contrib import admin
from .models import Govern, City
# Register your models here.
admin.site.register(Govern)


class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]
    
admin.site.register(City, CityAdmin)
