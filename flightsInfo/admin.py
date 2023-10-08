from django.contrib import admin
from .models import Bus, Appointments

class AppointmentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Appointments._meta.fields]
    
class BusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bus._meta.fields]


admin.site.register(Bus, BusAdmin)
admin.site.register(Appointments, AppointmentsAdmin)