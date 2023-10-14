from django.contrib import admin

from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    #readonly_fields = []
    list_display = ['user_name', 'user_phone', 'flight_move_from', 'flight_move_to', 'flight_date', 'flight_time']

    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = 'User Name'

    def user_phone(self, obj):
        return obj.user.phone
    user_phone.short_description = 'User Phone'

    def flight_move_from(self, obj):
        return obj.flight.move_from
    flight_move_from.short_description = 'Move From'

    def flight_move_to(self, obj):
        return obj.flight.move_to
    flight_move_to.short_description = 'Move To'

    def flight_date(self, obj):
        return obj.flight.date
    flight_date.short_description = 'Date'

    def flight_time(self, obj):
        return obj.flight.time
    flight_time.short_description = 'Time'
    
    
    
admin.site.register(Reservation, ReservationAdmin)