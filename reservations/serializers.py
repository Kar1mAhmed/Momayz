from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='flight.program.move_from')
    move_to = serializers.CharField(source='flight.program.move_to')
    duration = serializers.CharField(source='flight.program.duration')
    class Meta:
        model = Reservation
        fields = "__all__"


