from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('locations/', include('locations.urls')),
    path('otp/', include('otp.urls')),
    path('QA/', include('QA.urls'))
]
