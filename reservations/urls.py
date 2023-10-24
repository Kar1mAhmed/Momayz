from django.urls import path
from .views import book_one_flight, get_my_reservation, edit_reservation, book_package

urlpatterns = [
    path('one-flight/', book_one_flight),
    path('mine/', get_my_reservation),
    path('edit/', edit_reservation),
    path('package/', book_package),
]
