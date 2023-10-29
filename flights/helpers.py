from django.utils import timezone
from datetime import datetime, timedelta
import pytz

from .models import Flight, Program


def create_new_flights_for_all_programs(date):
    programs = Program.objects.all()
    for program in programs:
        create_flight(program, date)


def create_flight(program, date):
    for appointment in program.move_at.all():
        new_flight = Flight.objects.create(program=program, date=date, time=appointment.time)
        new_flight.save()


def delete_old_flights(passed_days=1):
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date()
    deletion_date = current_date - timedelta(days=passed_days)

    # Delete old flights
    Flight.objects.filter(date__lt=deletion_date).delete()



def get_next_30_dates(start_date):
    # Convert the start_date to a datetime object
    date = datetime.strptime(start_date, '%Y-%m-%d')

    next_dates = []

    for _ in range(31):
        if date.weekday() != 4: # skip friday
            next_dates.append(date.strftime('%Y-%m-%d'))
        date += timedelta(days=1)

    return next_dates