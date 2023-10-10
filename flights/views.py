from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Flight, Program

def create_flight(program, date):
    for appointment in program.move_at.all():
        new_flight = Flight.objects.create(details=program, date=date, time=appointment.time)
        new_flight.save()


@api_view(['POST'])
def add_flight(request):
    flight_id = request.GET.get('pk')
    program = Program.objects.get(pk=flight_id)
    create_flight(program=program, date='2023-10-20')
    return Response({"detail": "flight Created"}, status=status.HTTP_200_OK)