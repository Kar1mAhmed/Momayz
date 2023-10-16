from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .models import Reservation
from flights.models import Flight




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
    

    reservation = Reservation.objects.create(user=user, flight=flight)

    # Check if the reservation was created successfully
    if reservation is not None:
        return Response({'detail': 'تم حجز الرحلة بنجاح.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'detail': 'حدث خطأ أثناء الحجز.'}, status=status.HTTP_400_BAD_REQUEST)
