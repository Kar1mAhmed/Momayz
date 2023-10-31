from celery import shared_task
from QA.models import QA
from flights.helpers import delete_old_flights
from reservations.helpers import delete_old_reservations
import logging
logger = logging.getLogger(__name__)


@shared_task(bind=True)
def midnight_call(self, reservation_days, flights_days):
    logger.info("Task my_task has started.")
    print("RUNNING MID NIGHT")
    delete_old_reservations(reservation_days)
    delete_old_flights(flights_days)
    

@shared_task(bind=True)
def test_func(self):
    QA.objects.create(A='DoIT', Q='Please')
    print("DO " * 10)