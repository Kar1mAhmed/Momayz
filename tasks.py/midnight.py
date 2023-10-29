from celery import shared_task

from flights.helpers import delete_old_flights
from reservations.helpers import delete_old_reservations


@shared_task
def midnight_call(reservation_days, flights_days):
    delete_old_reservations(reservation_days)
    delete_old_flights(flights_days)