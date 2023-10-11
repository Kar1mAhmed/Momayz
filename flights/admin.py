from django.contrib import admin
from .models import Flight, Program
from django.db.models import Q


class FlightAdmin(admin.ModelAdmin):
    readonly_fields = ['details', 'available_seats']
    list_display = ['move_from', 'move_to', 'date', 'time', 'available_seats', 'seats_count', 'cancelled']
    list_filter = ["details__move_from", "details__move_to",  "time", "cancelled", 'date']
    search_fields = ["details__move_from__name", "details__move_to__name", "date", "time", "cancelled"] 
    
    
    
    def get_search_results(self, request, queryset, search_term):
        lookup = (
            Q(details__move_from__name__icontains=search_term) |
            Q(details__move_to__name__icontains=search_term) |
            Q(date__icontains=search_term) |
            Q(time__icontains=search_term) 
            )
        
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset.filter(lookup), use_distinct
    
    def move_from(self, obj):
        return obj.details.move_from
    
    def move_to(self, obj):
        return obj.details.move_to
    
    
class ProgramDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'move_from', 'move_to', 'bus', 'duration', 'get_move_at']
    
    def get_move_at(self, obj):
        appointments = obj.move_at.all()
        if appointments:
            return ", ".join([appointment.time.strftime('%I:%M %p') for appointment in appointments])
        else:
            return ""
    get_move_at.short_description = 'Move At'


admin.site.register(Flight, FlightAdmin)
admin.site.register(Program, ProgramDetailsAdmin)