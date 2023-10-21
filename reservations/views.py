from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.db import transaction
from django.utils import timezone

from datetime import datetime, timedelta
import pytz



from .models import Reservation
from flights.models import Flight
from flightsInfo.models import Package

from .serializers import ReservationSerializer
from flights.serializers import FlightSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_reservation(request):
    user = request.user
    cairo_timezone = pytz.timezone('Africa/Cairo')
    today = timezone.now().astimezone(cairo_timezone).date()
    my_flights = Reservation.objects.filter(user=user, flight__date__gte=today)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reserve_package(request):
    package_id = request.data['package_id']
    days = request.data['days']
    package = Package.objects.get(pk=package_id)
    
    if request.user.credits < package.price:
        return Response({'detail': 'No enough credits.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(days) != package.num_of_flights / 4:
        return Response({'details': f'This package is {int(package.num_of_flights / 4)} days per week'})
    
    flights = get_flights(days, request.user)
    
    with transaction.atomic():
        for flight in flights:
            try:
                Reservation.objects.create(user=request.user, flight=flight)
            except Exception as e:
                flight_serialized = FlightSerializer(flight)
                return Response({
                    'detail': e,
                    'error_at_flight': flight_serialized.data},
                    status=status.HTTP_400_BAD_REQUEST)
        
    return Response({'detail': 'Package Reserved successfully.'})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_reservation(request):
    user = request.user
    reservation_to_cancel = request.data['reservation_to_cancel']
    flight_to_reserve_id = request.data['flight_to_reserve']
    
    reservation_to_cancel = Reservation.objects.get(pk=reservation_to_cancel, user=user)
    
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


def get_flights(days, user):
    '''
        the idea to get the flights of the days user picked and reserve it for 4 weeks ahead.
    '''
    flights = []
    for day in days:
        dates_of_day = get_dates(day['day'])
        for date in dates_of_day:
            # The Flight that goes from user Home to Collage
            flights.append(Flight.objects.get(date=date, program__move_from=user.city,program__move_at=day['go_at']))
            # The Flight that goes from Collage to user destination 
            flights.append(Flight.objects.get(date=date, program__move_to=user.city, program__move_at=day['return_at']))
    return flights


def get_dates(base_dates):
    dates_to_reserve = []
    dates_to_reserve.append(base_dates) # append the base date
    for num_of_weeks in range(1,4): # To reserve the same day after 1,2,3 weeks
        dates_to_reserve.append(date_after_num_of_weeks(base_dates, num_of_weeks))
    return dates_to_reserve


def date_after_num_of_weeks(date, num_weeks):
    # Convert the given date to a datetime object
    date_format = '%Y-%m-%d'
    given_date_datetime = datetime.strptime(date, date_format)

    # Calculate the date one week (7 days) after the given date
    days= num_weeks * 7
    one_week_after = given_date_datetime + timedelta(days=days)

    # Format the result as 'YYYY-MM-DD' again
    one_week_after_formatted = one_week_after.strftime(date_format)
    return one_week_after_formatted