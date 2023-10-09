from django.contrib import admin
from .models import Flight, Program


class FlightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Flight._meta.fields]
    
class ProgramDetailsAdmin(admin.ModelAdmin):
    list_display = ['move_from', 'move_to', 'bus', 'duration', 'get_move_at']
    
    def get_move_at(self, obj):
        appointments = obj.move_at.all()
        if appointments:
            return ", ".join([appointment.time.strftime('%I:%M %p') for appointment in appointments])
        else:
            return ""
    get_move_at.short_description = 'Move At'


admin.site.register(Flight, FlightAdmin)
admin.site.register(Program, ProgramDetailsAdmin)