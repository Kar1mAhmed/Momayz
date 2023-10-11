from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='details.move_from')
    move_to = serializers.CharField(source='details.move_to')
    duration = serializers.CharField(source='details.duration')
    class Meta:
        model = Flight
        fields = ['id', 'date', 'time', 'taken_seats', 'total_seats',
                    'move_from', 'move_to', 'duration', 'price']


