from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.utils import timezone
from datetime import  timedelta

import pytz

from .models import Flight, Program
from flightsInfo.models import Appointments, Day

from .helpers import create_flight, get_next_30_dates, create_flights_all_programs
from settings.helpers import notify_flight


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



@api_view(['POST'])
def test_not(request):
    times = ['07:00:00', '08:00:00', '09:30:00', '10:30:00', '12:00:00', '13:30:00', '15:00:00', '16:30:00']

    # Get the list of days
    days = Day.objects.all()

    # Create appointments for each day and time combination
    for day in days:
        for time in times:
            appointment = Appointments.create(day=day, time=time)
            appointment.save()
            
    return Response({'detail': 'Dogy'}, status=status.HTTP_201_CREATED)
            
            
@api_view(['POST'])
def create_all_programs_30(request):
    cairo_timezone = pytz.timezone('Africa/Cairo')
    today_date = timezone.now().astimezone(cairo_timezone).date()
    
    for i in range(31):
        date = today_date + timedelta(days=i)
        create_flights_all_programs(date)
    
    return Response({'detail': 'Created'}, status=status.HTTP_201_CREATED)