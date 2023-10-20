from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import models

from django.db.models import Q

from django.utils import timezone
from datetime import date, timedelta

from .models import Flight, Program
from .serializers import FlightSerializer




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_flights(request):
    user = request.user 
    city = user.city
    
    current_date = date.today()
    #current_time = timezone.now().time()
    
    
    flights = Flight.objects.filter(
    Q(program__move_from=city) | Q(program__move_to=city), 
    cancelled=False,
    taken_seats__lt=models.F('total_seats'),
    date=current_date
    #time__gt=current_time
    )

    data_serialized = FlightSerializer(flights, many=True)
    return Response(data_serialized.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tomorrow_flights(request):
    user = request.user 
    city = user.city
    
    current_date = date.today() + timedelta(days=1)

    flights = Flight.objects.filter(
    Q(program__move_from=city) | Q(program__move_to=city), 
    cancelled=False,
    taken_seats__lt=models.F('total_seats'),
    date=current_date,
    )

    data_serialized = FlightSerializer(flights, many=True)
    return Response(data_serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def flights_by_date(request):
    user = request.user 
    city = user.city
    
    date = request.GET.get('date')

    flights = Flight.objects.filter(
    Q(program__move_from=city) | Q(program__move_to=city), 
    cancelled=False,
    taken_seats__lt=models.F('total_seats'),
    date=date,
    )

    data_serialized = FlightSerializer(flights, many=True)
    return Response(data_serialized.data, status=status.HTTP_200_OK)




def create_flight(program, date):
    for appointment in program.move_at.all():
        new_flight = Flight.objects.create(program=program, date=date, time=appointment.time)
        new_flight.save()


@api_view(['POST'])
def add_flight(request):
    flight_id = request.data['pk']
    date = request.data['date']
    
    program = Program.objects.get(pk=flight_id)
    create_flight(program=program, date=date)
    return Response({"detail": "flight Created"}, status=status.HTTP_200_OK)