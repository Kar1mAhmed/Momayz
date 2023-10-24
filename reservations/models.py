from django.db import models, transaction


from users.models import User
from flights.models import Flight
from flightsInfo.models import Package



class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    reserved_at = models.DateTimeField(auto_now_add=True)
    seat_number = models.SmallIntegerField()
    package = models.ForeignKey(Package, on_delete=models.PROTECT, null=True, blank=True)

    
    class Meta:
        ordering = ['flight__date', 'flight__time']
        unique_together = ('flight', 'seat_number')

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                seat_number = self._get_seat_number(self.flight, self.user.gender)
                if seat_number:
                    if not self.package:
                        credits_deducted = self.user.deduct_credits(self.flight.program.price)
                    else:
                        credits_deducted = True
                    if credits_deducted:
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
                if self.package:
                    credits_to_refund = self.package.price / self.package.num_of_flights
                    self.user.refund_credits(credits_to_refund)
                else:
                    credits_to_refund = self.flight.program.price
                    self.user.refund_credits(self.flight.program.price)
                return super().delete(*args, **kwargs)
        except Exception as e:
            raise e
    
    
    def replace(self, flight_to_reserve_id):
        flight_to_reserve = Flight.objects.get(pk=flight_to_reserve_id)
        
        
        if flight_to_reserve.taken_seats >= flight_to_reserve.total_seats:
            raise ValueError('No enough seats')
        
        if flight_to_reserve.program.move_from != self.flight.program.move_from \
            or flight_to_reserve.program.move_to != self.flight.program.move_to:
                raise ValueError('The flight should have the same destinations.')
        
        try:
            with transaction.atomic():
                self.flight.decrement_taken_seats()
                flight_to_reserve.increment_taken_seats()
                
                seat = self._get_seat_number(flight_to_reserve, self.user.gender)
                
                self.flight = flight_to_reserve
                self.seat_number = seat
                self.save()
                return self
                
        except Exception as e:
            raise str(e)
        
    def _get_seat_number(self, flight, gender): 
        with transaction.atomic():
            if flight.taken_seats >= flight.total_seats:
                return None
            
            reserved_seat_numbers = set(Reservation.objects.filter(flight=flight) \
                                        .values_list('seat_number', flat=True))
            
            # separate males from females
            if gender == 'Female': 
                start = 1
                end = flight.total_seats + 1
                move = 1
            else:
                start = flight.total_seats 
                end = 0
                move = -1
                
            for seat_number in range(start, end, move):
                    if seat_number not in reserved_seat_numbers:
                        return seat_number
            return None