from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='flight.details.move_from')
    move_to = serializers.CharField(source='flight.details.move_to')
    duration = serializers.CharField(source='flight.details.duration')
    class Meta:
        model = Reservation
        fields = "__all__"


