from django.urls import path
from .views import CityView, GovernView

urlpatterns = [
    path('govern/', GovernView.as_view()),
    path('city/', CityView.as_view()),
]
