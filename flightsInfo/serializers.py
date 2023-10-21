from rest_framework import serializers
from .models import Package, Appointments

class PackageSerializer(serializers.ModelSerializer):
    # days_per_week = serializers.SerializerMethodField()
    class Meta:
        model = Package
        fields = '__all__'

    # def get_days_per_week(self, obj):
    #     return int(obj.num_of_flights / 4)


class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'