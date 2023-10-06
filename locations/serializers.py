from .models import Govern, City
from rest_framework import serializers


class GovernSerializer(serializers.ModelSerializer):
    class Meta:
        model = Govern
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'