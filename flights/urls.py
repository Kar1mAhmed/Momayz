from django.urls import path
from .views import add_flight, today_flights, tomorrow_flights, flights_by_date, add_flight_for_next_month

urlpatterns = [
    path('', add_flight),
    path('add-30-days/', add_flight_for_next_month),
    path('today/', today_flights),
    path('tomorrow/', tomorrow_flights),
    path('by-date/', flights_by_date)
]
