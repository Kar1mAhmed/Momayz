from django.contrib import admin
from .models import Flight, Program
from django.db.models import Q


class FlightAdmin(admin.ModelAdmin):
    readonly_fields = ['program', 'taken_seats']
    list_display = ['move_from', 'move_to', 'date', 'time', 'taken_seats', 'total_seats', 'canceled']
    list_filter = ["program__move_from", "program__move_to",  "time", "canceled", 'date', 'program__price']
    search_fields = ["program__move_from__name", "program__move_to__name", "date", "time", "canceled"] 
    
    
    
    def get_search_results(self, request, queryset, search_term):
        lookup = (
            Q(program__move_from__name__icontains=search_term) |
            Q(program__move_to__name__icontains=search_term) |
            Q(date__icontains=search_term) |
            Q(time__icontains=search_term) 
            )
        
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset.filter(lookup), use_distinct
    
    def move_from(self, obj):
        return obj.program.move_from
    
    def move_to(self, obj):
        return obj.program.move_to
    
    def price(self, obj):
        return obj.program.price
    
    
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'move_from', 'move_to', 'bus', 'duration', 'get_move_at', 'price']
    
    def get_move_at(self, obj):
        appointments = obj.move_at.all()
        if appointments:
            return ", ".join([appointment.time.strftime('%I:%M %p') for appointment in appointments])
        else:
            return ""
    get_move_at.short_description = 'Move At'


admin.site.register(Flight, FlightAdmin)
admin.site.register(Program, ProgramAdmin)