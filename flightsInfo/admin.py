from django.contrib import admin
from .models import Bus, Appointments, Package, Day

class AppointmentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Appointments._meta.fields]
    
class BusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bus._meta.fields]
    
class PackageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Package._meta.fields]


admin.site.register(Bus, BusAdmin)
admin.site.register(Appointments, AppointmentsAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Day)





