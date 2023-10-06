from django.urls import path
from .views import QAView

urlpatterns = [
    path('', QAView.as_view()) ,
]
