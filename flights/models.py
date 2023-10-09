from django.db import models
from locations.models import Area
from flightsInfo.models import Appointments, Bus

class FlightDetails(models.Model):
    move_from = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="move_from")
    move_to = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="move_to")
    move_at = models.ManyToManyField(Appointments)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    duration = models.CharField(max_length=8)


class FlightManager(models.Manager):
    def create(self, **kwargs):
        # Check if seats_count and available_seats are not provided, and if so, set them based on related models
        if 'seats_count' not in kwargs and 'available_seats' not in kwargs:
            kwargs['seats_count'] = kwargs['details'].bus.seats_count
            kwargs['available_seats'] = kwargs['details'].bus.seats_count

        # Create a new Flight instance
        flight = self.model(**kwargs)
        flight.save(using=self._db)
        return flight


class Flight(models.Model):
    details = models.ForeignKey(FlightDetails, on_delete=models.PROTECT)
    date = models.DateField()
    available_seats = models.SmallIntegerField()
    seats_count = models.SmallIntegerField()
    cancelled = models.BooleanField(default=False)
    
    objects = FlightManager()
