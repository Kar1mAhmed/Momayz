from django.urls import path
from .views import get_chat

urlpatterns = [
    path('', get_chat),

]
