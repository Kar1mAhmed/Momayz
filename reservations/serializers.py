from rest_framework import serializers
from .models import Reservation, Subscription

class ReservationSerializer(serializers.ModelSerializer):
    move_from = serializers.CharField(source='flight.program.move_from')
    move_to = serializers.CharField(source='flight.program.move_to')
    duration = serializers.CharField(source='flight.program.duration')
    date = serializers.CharField(source='flight.date')
    price = serializers.CharField(source='flight.program.price')
    time = serializers.CharField(source='flight.time')
    class Meta:
        model = Reservation
        exclude = ['reserved_at', 'user', 'flight']


class SubscriptionSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name')
    total_reservations = serializers.CharField(source='total_reservations')
    class Meta:
        model = Subscription
        exclude = ['package', 'user', 'started_at']