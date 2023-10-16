from django.urls import path
from .views import reserve_one_flight

urlpatterns = [
    path('one-flight/', reserve_one_flight),
]
