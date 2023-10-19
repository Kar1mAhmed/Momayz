from django.contrib import admin

from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    #readonly_fields = []
    list_display = ['user_name', 'user_username', 'flight_move_from',
                    'flight_move_to', 'flight_date', 'flight_time']


    actions = ['immediate_delete']

    def immediate_delete(self, request, queryset):
        for item in queryset:
            item.delete()
        self.message_user(
            request,
            f"items deleted.",
        )

    immediate_delete.short_description = "Delete selected items "
    
    
    def get_actions(self, request):
        # Override the get_actions method to exclude the delete action
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions
    
    def user_name(self, obj):
        return obj.user.name
    
    user_name.short_description = 'User Name'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User Phone'

    def flight_move_from(self, obj):
        return obj.flight.program.move_from
    flight_move_from.short_description = 'Move From'

    def flight_move_to(self, obj):
        return obj.flight.program.move_to
    flight_move_to.short_description = 'Move To'

    def flight_date(self, obj):
        return obj.flight.date
    flight_date.short_description = 'Date'

    def flight_time(self, obj):
        return obj.flight.time
    flight_time.short_description = 'Time'
    
    
    
admin.site.register(Reservation, ReservationAdmin)