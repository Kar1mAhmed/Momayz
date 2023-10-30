from django.urls import path
from .views import get_chat, test


urlpatterns = [
    path('', get_chat),
    path('test/', test)

]
