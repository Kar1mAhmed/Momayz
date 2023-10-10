from django.urls import path
from .views import add_flight

urlpatterns = [
    path('', add_flight),
    
]
