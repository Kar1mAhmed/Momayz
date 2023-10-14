from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


from .models import Reservation
from flights.models import Flight




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def one_flight(request):
    user = request.user
    flight_id = request.data['flight_id']
    
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        return Response({'detail': "لم يتم العثور علي الرحلة."}, status=status.HTTP_404_NOT_FOUND)
    
    if flight.price > user.credits:
        return Response({'detail' : 'لا يتوفر رصيد كافي لحجز الرحلة.'}, status=status.HTTP_402_PAYMENT_REQUIRED)
    
    seat_number = flight.reserve()
    
    if not seat_number:
        return Response({'detail': 'لم يتبقى أي مقاعد في الرحلة.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    try:
        with transaction.atomic():
            user.credits -= flight.price
            user.save(update_fields=['credits'])

            Reservation.objects.create(user=user, seat_number=seat_number, flight=flight)
            return Response({'detail': 'تم حجز الرحلة بنجاح.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'detail': 'حدثت مشكلة أثناء الحجز برجاء المحاولة من جديد.'}, status=status.HTTP_400_BAD_REQUEST)

