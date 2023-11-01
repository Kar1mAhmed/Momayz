from django.urls import path
from .views import today_flights, tomorrow_flights, flights_by_date

from .dev_views import add_flight_for_next_month, test_not, add_flight, create_all_programs_30



urlpatterns = [
    path('today/', today_flights),
    path('tomorrow/', tomorrow_flights),
    path('by-date/', flights_by_date),
]


# DEV URLS
urlpatterns+= [
    path('notify_flight/', test_not),
    path('add-30-days/', add_flight_for_next_month),
    path('', add_flight),
    path('creator/', create_all_programs_30)
]
