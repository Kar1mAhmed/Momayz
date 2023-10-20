from django.urls import path
from .views import add_flight, today_flights, tomorrow_flights, flights_by_date

urlpatterns = [
    path('', add_flight),
    path('today/', today_flights),
    path('tomorrow/', tomorrow_flights),
    path('by-date/', flights_by_date)
]
