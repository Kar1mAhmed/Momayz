from django.db import models
from django.db.models import F
from users.models import User
from flights.models import Flight
from django.db import transaction




class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    reserved_at = models.DateTimeField(auto_now_add=True)
    seat_number = models.SmallIntegerField()



    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                if self.user.credits < self.flight.price:
                    raise Exception('no enough credits')
                
                if self.flight.taken_seats < self.flight.total_seats:
                    updated_seats = Flight.objects.filter(pk=self.flight.pk, taken_seats__lt=F('total_seats')).update(taken_seats=F('taken_seats') + 1)
                    
                    if updated_seats == 1:
                        self.user.credits -= self.flight.price
                        self.user.save(update_fields=['credits'])
                        return super().save(*args, **kwargs)
                    else:
                        raise Exception("seats not enough.")
                else:   
                    raise Exception("seats not enough.")

        
    
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            updated_seats = Flight.objects.filter(
                pk=self.flight.pk, taken_seats__gt=0
            ).update(taken_seats=F('taken_seats') - 1)

            if updated_seats == 1:
                return super().delete(*args, **kwargs)
            else:
                raise Exception("No seats to decrement.")