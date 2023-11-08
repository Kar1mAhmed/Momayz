from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.utils import timezone
from datetime import  timedelta

import pytz

from .models import Flight, Program
from flightsInfo.models import Appointments, Day, Bus, Package
from locations.models import Area, Govern

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
def do(request):
    flights = Flight.objects.all()
    flights.delete()
    return Response({"detail": "Done"}, status=status.HTTP_200_OK)




@api_view(['POST'])
def test_not(request):
    times_go = ['07:00:00', '08:00:00', '09:30:00', '10:30:00']
    times_return = ['12:00:00', '13:30:00', '15:00:00', '16:30:00']
    days = Day.objects.all().exclude(name='Friday')

    cities = Area.objects.filter(city=True)
    collage = Area.objects.filter(city=False).first()
    asyt = Govern.objects.all().first()
    bus = Bus.objects.all().first()
    
    appointments_go = []
    for day in days:
        for time in times_go:
            appointments_go.append(Appointments.objects.get(time=time, day=day))
            
    for city in cities:
        program = Program.objects.create(
            govern=asyt,
            move_from=city,
            move_to=collage,
            bus=bus,
            duration="00:30:00",
            price=25
        )
        program.move_at.set(appointments_go)  # Set the many-to-many relationship

    
    appointments_return = []
    for day in days:
        for time in times_return:
            appointments_return.append(Appointments.objects.get(time=time, day=day))
    for city in cities:
        program = Program.objects.create(
            govern=asyt,
            move_from=collage,
            move_to=city,
            bus=bus,
            duration="00:30:00",
            price=25
        )
        program.move_at.set(appointments_return)  
    
            
    return Response({'detail': 'Dogy'}, status=status.HTTP_201_CREATED)
            
            
@api_view(['POST'])
def create_all_programs_30(request):
    
    create_flights_all_programs()
    
    return Response({'detail': 'Created'}, status=status.HTTP_201_CREATED)