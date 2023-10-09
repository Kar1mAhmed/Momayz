from django.contrib import admin
from .models import Flight, Program


class FlightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Flight._meta.fields]
    
class ProgramDetailsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Program._meta.fields]
    


admin.site.register(Flight, FlightAdmin)
admin.site.register(Program, ProgramDetailsAdmin)