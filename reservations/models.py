from django.db import models
from django.db.models import F
from users.models import User
from flights.models import Flight


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    reserved_at = models.DateTimeField(auto_now_add=True)
    seat_number = models.SmallIntegerField()

    
    def delete(self, *args, **kwargs):
        # Decrement the taken_seats count using F() expressions and update()
        self.flight.taken_seats = F('taken_seats') - 1
        self.flight.save(update_fields=['taken_seats'])
        return super().delete(*args, **kwargs)