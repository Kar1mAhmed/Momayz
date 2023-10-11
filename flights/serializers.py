from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='details.move_from')
    move_to = serializers.CharField(source='details.move_to')
    duration = serializers.CharField(source='details.duration')
    class Meta:
        model = Flight
        fields = ['id', 'date', 'time', 'available_seats', 'seats_count',
                    'move_from', 'move_to', 'duration', 'price']


