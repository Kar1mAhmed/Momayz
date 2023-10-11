from django.urls import path
from .views import add_flight, today_flights, tomorrow_flights

urlpatterns = [
    path('', add_flight),
    path('today/', today_flights),
    path('tomorrow/', tomorrow_flights)
]
