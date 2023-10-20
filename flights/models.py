from django.db import models, transaction

from reservations.models import Reservation
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
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField(default="00:00:00")
    taken_seats = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    total_seats = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    cancelled = models.BooleanField(default=False)
    price = models.SmallIntegerField(validators=[MinValueValidator(0)], default=25)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if str(self.time) == '00:00:00':
                self.time = self.program.move_at.first().time
            if not self.total_seats:
                self.total_seats = self.program.bus.seats
            if not self.price:
                self.price = self.program.price
            
        super(Flight, self).save(*args, **kwargs)

    def get_seat_number(self): 
        with transaction.atomic():
            if self.taken_seats >= self.total_seats:
                return None
            
            reserved_seat_numbers = set(Reservation.objects.filter(flight=self) \
                                        .values_list('seat_number', flat=True))
            
            for seat_number in range(1, self.total_seats + 1):
                    if seat_number not in reserved_seat_numbers:
                        self.taken_seats+=1
                        return seat_number
            return None

    def increment_taken_seats(self):
        self.taken_seats += 1
        self.save()
        
    def decrement_taken_seats(self):
        self.taken_seats -= 1
        self.save()

    class Meta:
        ordering = ['date', 'time']

        
    def __str__(self) -> str:
        return f"{self.program.move_from} إلي {self.program.move_to} ({self.date} | {self.time})"
