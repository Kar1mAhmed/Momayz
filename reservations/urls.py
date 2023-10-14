from django.urls import path
from .views import one_flight

urlpatterns = [
    path('one-flight/', one_flight),
]
