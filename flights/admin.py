from django.contrib import admin
from .models import Flight, FlightDetails


class FlightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Flight._meta.fields]
    
class FlightDetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FlightDetails._meta.fields]
    


admin.site.register(Flight, FlightAdmin)
admin.site.register(FlightDetails, FlightDetailsAdmin)