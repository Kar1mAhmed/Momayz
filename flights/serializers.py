from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='program.move_from')
    move_to = serializers.CharField(source='program.move_to')
    duration = serializers.CharField(source='program.duration')
    price = serializers.CharField(source='program.price')
    flight_type = serializers.SerializerMethodField()
    class Meta:
        model = Flight
        fields = ['id', 'date', 'time', 'taken_seats', 'total_seats',
                    'move_from', 'move_to', 'duration', 'price', 'flight_type']

    def get_flight_type(self, obj):
        move_to = obj.program.move_to
        
        if move_to.name == 'الجامعة':
            return 'ذهاب'
        else:
            return 'عودة'
