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




class Flight(models.Model):
    details = models.ForeignKey(Program, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField(default="00:00:00")
    available_seats = models.SmallIntegerField(default=0)
    seats_count = models.SmallIntegerField(default=0)
    cancelled = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.time :
                self.time = self.details.move_at.first().time
            if not self.available_seats:
                self.available_seats = self.details.bus.seats
            if not self.seats_count:
                self.seats_count = self.details.bus.seats
        
        super(Flight, self).save(*args, **kwargs)

        
    def __str__(self) -> str:
        return f"{self.details.move_from} to {self.details.move_to} ({self.date}|{self.time})"
