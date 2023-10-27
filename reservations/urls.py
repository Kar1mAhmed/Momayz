from django.urls import path
from .views import book_one_flight, my_reservation, edit_reservation, book_package, my_package_status

urlpatterns = [
    path('one-flight/', book_one_flight),
    path('mine/', my_reservation),
    path('edit/', edit_reservation),
    path('package/', book_package),
    path('subscription/', my_package_status),
]
