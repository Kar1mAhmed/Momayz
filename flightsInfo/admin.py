from django.contrib import admin
from .models import Bus, Appointments

class AppointmentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Appointments._meta.fields]
    
class BusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bus._meta.fields]


admin.site.register(Bus, BusAdmin)
admin.site.register(Appointments, AppointmentsAdmin)



########## UN REGISTER SOME USELESS MODELS FOR ADMIN ######################
from django.contrib.sites.models import Site
admin.site.unregister(Site)

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)


