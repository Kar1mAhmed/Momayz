from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .models import Reservation
from flights.models import Flight
from .serializers import ReservationSerializer

from django.utils import timezone
import pytz


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_reservation(request):
    user = request.user
    my_flights = Reservation.objects.filter(user=user)
    serialized_data = ReservationSerializer(my_flights, many=True)
    return Response(serialized_data.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reserve_one_flight(request):
    user = request.user
    flight_id = request.data['flight_id']
    
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        return Response({'detail': "لم يتم العثور علي الرحلة."}, status=status.HTTP_404_NOT_FOUND)
    
    if flight.price > user.credits:
        return Response({'detail' : 'لا يتوفر رصيد كافي لحجز الرحلة.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        reservation = Reservation.objects.create(user=user, flight=flight)
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the reservation was created successfully
    if reservation is not None:
        serialized_data = ReservationSerializer(reservation)
        return Response({'detail': 'تم حجز الرحلة بنجاح.',
                        'reservation_info' : serialized_data.data},
                        status=status.HTTP_201_CREATED)
    else:
        return Response({'detail': 'حدث خطأ أثناء الحجز.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_reservation(request):
    user = request.user
    reservation_id = request.data['reservation_id']
    reservation = Reservation.objects.get(pk=reservation_id, user=user)
    
    #check if the Flight is today
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date_in_cairo = timezone.now().astimezone(cairo_timezone).date()
    if reservation.flight.date == current_date_in_cairo:
        return Response({'detail': 'لا يمكن تعديل الرحلة, موعد الأنطلاق اليوم.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    return Response({'detail': "A7oooo"})