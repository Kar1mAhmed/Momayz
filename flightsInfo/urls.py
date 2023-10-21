from django.urls import path
from .views import get_packages

urlpatterns = [
    path('packages/', get_packages),
]
