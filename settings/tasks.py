from celery import shared_task

from flights.helpers import delete_old_flights, create_flights_all_programs
from reservations.helpers import delete_old_reservations

from django.utils import timezone

from datetime import  timedelta
import pytz

from .helpers import *

from flights.models import Flight

@shared_task(bind=True)
def midnight_call(self, reservation_days=1, flights_days=1):
    delete_old_reservations(reservation_days)
    delete_old_flights(flights_days)
    
    cairo_timezone = pytz.timezone('Africa/Cairo')
    today_date = timezone.now().astimezone(cairo_timezone).date()
    date_after_30 = today_date + timedelta(days=30)
    
    create_flights_all_programs(date_after_30)
    


@shared_task(bind=True)
def notify_before_30min(self):
    cairo_timezone = pytz.timezone('Africa/Cairo')
    today_date = timezone.now().astimezone(cairo_timezone).date()
    Flights = Flight.objects.filter(date=today_date)
    
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_time =  timezone.now().astimezone(cairo_timezone).time()
    time_in_30_minutes = current_time + timedelta(minutes=30)

    for flight in Flights:
        if flight.time < time_in_30_minutes and not flight.notified:
            notify_flight(flight.pk)
            flight.notified = True
            flight.save()