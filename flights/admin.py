from django.contrib import admin
from .models import Flight, Program
from django.db.models import Q


class FlightAdmin(admin.ModelAdmin):
    readonly_fields = ['program']
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
    list_display = ['move_from', 'move_to', 'bus', 'duration','price']
    readonly_fields = ['move_from', 'move_to']
    


admin.site.register(Flight, FlightAdmin)
admin.site.register(Program, ProgramAdmin)