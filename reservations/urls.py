from django.urls import path
from .views import reserve_one_flight, get_my_reservation, edit_reservation

urlpatterns = [
    path('one-flight/', reserve_one_flight),
    path('mine/', get_my_reservation),
    path('edit/', edit_reservation)
]
