from django.contrib import admin
from django.urls import path
from .views import CityView, GovernView

urlpatterns = [
    path('govern/', CityView.as_view()),
    path('city/', GovernView.as_view()),
]
