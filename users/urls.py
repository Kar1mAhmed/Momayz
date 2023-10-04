from django.contrib import admin
from django.urls import path, include

from .views import *
urlpatterns = [
    path('<str:pk>', UserDetails.as_view()),
]