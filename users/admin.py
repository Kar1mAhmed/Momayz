from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'city', 'govern', 'credits']
    
    def govern(self, obj):
        return obj.city.govern


admin.site.register(User, UserAdmin)