from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

import pytz


from .models import Reservation, Subscription
from flights.models import Flight
from flightsInfo.models import Package

from .serializers import ReservationSerializer, SubscriptionSerializer
from flights.serializers import FlightSerializer

from .helpers import get_flights



class ReservationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *arg, **kwargs):
        user = request.user
        cairo_timezone = pytz.timezone('Africa/Cairo')
        today = timezone.now().astimezone(cairo_timezone).date()
        my_flights = Reservation.objects.filter(user=user, flight__date__gte=today)
        
        
        serialized_data = ReservationSerializer(my_flights, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        user = request.user
        flight_id = request.data['flight_id']
        
        try:
            flight = Flight.objects.get(pk=flight_id)
        except Flight.DoesNotExist:
            return Response({'detail': "لم يتم العثور علي الرحلة."}, status=status.HTTP_404_NOT_FOUND)
        
        if flight.program.price > user.credits:
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



class PackageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *arg, **kwargs):
        user = request.user
        subscriptions = Subscription.objects.filter(user=user)
        
        if subscriptions.count() == 0:
            return Response({
            "package_name": " لا يوجد اشتراك",
            "total_reservations": "0",
            "price": "0",
            "passed_reservations": 0,
            "first_flight_date": "",
            "last_flight_date": ""},status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = SubscriptionSerializer(subscriptions.first())
        return Response(serialized_data.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        package_id = request.data['package_id']
        days = request.data['days']
        
        try:
            package = Package.objects.get(pk=package_id)
        except ObjectDoesNotExist:
            return Response({'detail': 'Package doesn\'t exist.'})
        
        if request.user.credits < package.price:
            return Response({'detail': 'No enough credits.'}, status=status.HTTP_400_BAD_REQUEST)
        
        WEEKS_PER_MONTH = 4
        FLIGHT_PER_DAY = 2
        
        if len(days) * FLIGHT_PER_DAY != package.num_of_flights / WEEKS_PER_MONTH:
            return Response({'details': f'This package is {int(package.num_of_flights / WEEKS_PER_MONTH)} days per week'})
        
        flights = get_flights(days, request.user)
        
        if not flights or len(flights) != package.num_of_flights:
            return Response({'detail': 'something went wrong please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        
        last_flight = None
        try:
            with transaction.atomic():
                subscription = Subscription.objects.create(user=request.user, package=package)
                
                first_flight = None
                last_flight = None

                for flight in flights:
                    Reservation.objects.create(user=request.user, flight=flight, subscription=subscription)
                    if not first_flight or flight.date < first_flight.date:
                        first_flight = flight
                    if not last_flight or flight.date > last_flight.date:
                        last_flight = flight
                
                subscription.first_flight_date = first_flight.date if first_flight else timezone.now().date()
                subscription.last_flight_date = last_flight.date if last_flight else timezone.now().date()
                subscription.save()

                request.user.deduct_credits(package.price)
                
                
        except Exception as e:
            flight_with_error = FlightSerializer(last_flight)
            return Response({
                        'detail': str(e),
                        'error_at_flight': flight_with_error.data},
                        status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'Package Reserved successfully.'}, status=status.HTTP_201_CREATED)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_reservation(request):
    user = request.user
    reservation_to_cancel = request.data['reservation_to_cancel']
    flight_to_reserve_id = request.data['flight_to_reserve']
    
    try:
        reservation_to_cancel = Reservation.objects.get(pk=reservation_to_cancel, user=user)
    except ObjectDoesNotExist:
        return Response({'detail': 'Reservation not found.'}, status=status.HTTP_400_BAD_REQUEST)
    
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date_in_cairo = timezone.now().astimezone(cairo_timezone).date()
    if reservation_to_cancel.flight.date == current_date_in_cairo:
        return Response({'detail': 'لا يمكن تعديل الرحلة, موعد الأنطلاق اليوم.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        new_flight =reservation_to_cancel.replace(flight_to_reserve_id)
            
        serialized_reservation = ReservationSerializer(new_flight)
        return Response({'detail': 'تم تعديل موعد الرحلة بنجاح.',
                        'reservation': serialized_reservation.data}, status=status.HTTP_200_OK)
        
    except ValueError as e:
        return Response({'detail': 'فشل الحجز برجاء المحاولة مرة أخرى.'}, status=status.HTTP_200_OK)