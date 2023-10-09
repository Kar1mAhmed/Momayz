from django.db import models
from locations.models import Area
from flightsInfo.models import Appointments, Bus

class Program(models.Model):
    move_from = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="move_from")
    move_to = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="move_to")
    move_at = models.ManyToManyField(Appointments)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    duration = models.CharField(max_length=8)
    
    def __str__(self) -> str:
        return f"{self.move_from} to {self.move_to}"


class FlightManager(models.Manager):
    def create(self, **kwargs):
        # Check if seats_count and available_seats are not provided, and if so, set them based on related models
        if 'seats_count' not in kwargs:
            kwargs['seats_count'] = kwargs['details'].bus.seats_count
        
        if 'available_seats' not in kwargs:
            kwargs['available_seats'] = kwargs['details'].bus.seats_count
            
        if 'time' not in kwargs:
            kwargs['time'] = kwargs['details'].time.first()


        # Create a new Flight instance
        flight = self.model(**kwargs)
        flight.save(using=self._db)
        return flight


class Flight(models.Model):
    details = models.ForeignKey(Program, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    available_seats = models.SmallIntegerField(blank=True, null=True)
    seats_count = models.SmallIntegerField(blank=True, null=True)
    cancelled = models.BooleanField(default=False)
    
    objects = FlightManager()
    
    def __str__(self) -> str:
        return f"{self.details.move_from} to {self.details.move_to} ({self.date}|{self.time})"
