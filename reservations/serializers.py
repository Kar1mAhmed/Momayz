from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='flight.program.move_from')
    move_to = serializers.CharField(source='flight.program.move_to')
    duration = serializers.CharField(source='flight.program.duration')
    date = serializers.CharField(source='flight.date')
    price = serializers.CharField(source='flight.price')
    time = serializers.CharField(source='flight.time')
    class Meta:
        model = Reservation
        exclude = ['reserved_at', 'user', 'flight']


