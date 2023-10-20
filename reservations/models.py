from django.db import models
from users.models import User
from flights.models import Flight
from django.db import transaction




class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    reserved_at = models.DateTimeField(auto_now_add=True)
    seat_number = models.SmallIntegerField()

    class Meta:
        ordering = ['flight__date', 'flight__time']
        unique_together = ('flight', 'seat_number')

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                seat_number = self._get_seat_number(self.flight)
                if seat_number:
                    if self.user.deduct_credits(self.flight.price):
                        self.seat_number = seat_number
                        self.flight.increment_taken_seats()
                        return super().save(*args, **kwargs)
                    else:
                        raise ValueError("No enough credits.")
                else:
                    raise ValueError("Flight is full.")
        return super().save(*args, **kwargs)
        
    
    def delete(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.flight.decrement_taken_seats()
                self.user.refund_credits(self.flight.price)
                return super().delete(*args, **kwargs)
        except Exception as e:
            raise e
    
    
    def replace(self, flight_to_reserve_id):
        flight_to_reserve = Flight.objects.get(pk=flight_to_reserve_id)
        
        user_credits = self.user.credits + self.flight.price # user credits if reservation got cancelled
        if flight_to_reserve.price > user_credits:
            raise ValueError('No enough credits')
        
        if flight_to_reserve.taken_seats >= flight_to_reserve.total_seats:
            raise ValueError('No enough seats')
        
        if flight_to_reserve.program.move_from != self.flight.program.move_from \
            or flight_to_reserve.program.move_to != self.flight.program.move_to:
                raise ValueError('The flight should have the same destinations.')
        
        try:
            with transaction.atomic():
                self.flight.decrement_taken_seats()
                flight_to_reserve.increment_taken_seats()
                
                seat = self._get_seat_number(flight_to_reserve)
                
                self.flight = flight_to_reserve
                self.seat_number = seat
                self.save()
                return self
                
        except Exception as e:
            raise str(e)
        
    def _get_seat_number(self, flight): 
        with transaction.atomic():
            if flight.taken_seats >= flight.total_seats:
                return None
            
            reserved_seat_numbers = set(Reservation.objects.filter(flight=flight) \
                                        .values_list('seat_number', flat=True))
            
            for seat_number in range(1, flight.total_seats + 1):
                    if seat_number not in reserved_seat_numbers:
                        return seat_number
            return None