from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.db import models
from django.db.models import Q
from django.utils import timezone


from datetime import date, timedelta
import pytz


from .models import Flight, Program
from .serializers import FlightSerializer

from .helpers import create_flight, get_next_30_dates


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_flights(request):
    user = request.user 
    city = user.city
    
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date()
    #current_time = timezone.now().time()
    
    
    flights = Flight.objects.filter(
    Q(program__move_from=city) | Q(program__move_to=city), 
    canceled=False,
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
    
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date() + timedelta(days=1)

    flights = Flight.objects.filter(
    Q(program__move_from=city) | Q(program__move_to=city), 
    canceled=False,
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
    move_from = request.GET.get('move_from')
    move_to = request.GET.get('move_to')

    flights = Flight.objects.filter(
    Q(program__move_from__name=move_from) | Q(program__move_to__name=move_to), 
    canceled=False,
    taken_seats__lt=models.F('total_seats'),
    date=date,
    )

    data_serialized = FlightSerializer(flights, many=True)
    return Response(data_serialized.data, status=status.HTTP_200_OK)







@api_view(['POST'])
def add_flight(request):
    flight_id = request.data['pk']
    date = request.data['date']
    
    program = Program.objects.get(pk=flight_id)
    create_flight(program=program, date=date)
    return Response({"detail": "flight Created"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_flight_for_next_month(request):
    program_id = request.data['pk']
    
    program = Program.objects.get(pk=program_id)
    cairo_timezone = pytz.timezone('Africa/Cairo')
    today_date = timezone.now().astimezone(cairo_timezone).date()
    dates = get_next_30_dates(str(today_date))
    
    for date in dates:
        flights = Flight.objects.filter(program=program, date=date)
        if not flights.exists():
            create_flight(program=program, date=date)
            
    return Response({"detail": "flights Created"}, status=status.HTTP_200_OK)



