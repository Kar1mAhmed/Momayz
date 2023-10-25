from datetime import timedelta, datetime

from .models import Flight


def create_flight(program, date):
    for appointment in program.move_at.all():
        new_flight = Flight.objects.create(program=program, date=date, time=appointment.time)
        new_flight.save()
        
        

def get_next_30_dates(start_date):
    # Convert the start_date to a datetime object
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    next_dates = []

    for _ in range(30):
        next_dates.append(start_date.strftime('%Y-%m-%d'))
        start_date += timedelta(days=1)

    return next_dates