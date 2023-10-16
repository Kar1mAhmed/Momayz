from django.db import models
from locations.models import Area, Govern
from flightsInfo.models import Appointments, Bus

from django.core.validators import MinValueValidator



class Program(models.Model):
    govern = models.ForeignKey(Govern, on_delete=models.PROTECT, default=1)
    move_from = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="move_from")
    move_to = models.ForeignKey(Area, on_delete=models.PROTECT, related_name="move_to")
    move_at = models.ManyToManyField(Appointments)
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)
    duration = models.CharField(max_length=8)
    price = models.SmallIntegerField(validators=[MinValueValidator(0)], default=25)
    
    
    def __str__(self) -> str:
        return f"{self.move_from} إلي {self.move_to}"




class Flight(models.Model):
    details = models.ForeignKey(Program, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField(default="00:00:00")
    taken_seats = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    total_seats = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    cancelled = models.BooleanField(default=False)
    price = models.SmallIntegerField(validators=[MinValueValidator(0)], default=25)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if str(self.time) == '00:00:00':
                self.time = self.details.move_at.first().time
            if not self.total_seats:
                self.total_seats = self.details.bus.seats
            if not self.price:
                self.price = self.details.price
            
        super(Flight, self).save(*args, **kwargs)


        
    def __str__(self) -> str:
        return f"{self.details.move_from} إلي {self.details.move_to} ({self.date} | {self.time})"
