from django.db import models, transaction

from users.models import User
from flights.models import Flight
from flightsInfo.models import Package




class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT, db_index=True)
    reserved_at = models.DateTimeField(auto_now_add=True)
    seat_number = models.SmallIntegerField()
    subscription = models.ForeignKey('Subscription', on_delete=models.PROTECT, null=True, blank=True, db_index=True)

    
    class Meta:
        ordering = ['flight__date', 'flight__time']
        unique_together = ('flight', 'seat_number')

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                seat_number = self._get_seat_number(self.flight, self.user.gender)
                if seat_number:
                    if self._handel_credits():
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
                if self.subscription:
                    credits_to_refund = self.subscription.package.price / self.subscription.package.num_of_flights
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
        
        
    def _handel_credits(self):
        if not self.subscription:
            try:
                self.user.deduct_credits(self.flight.program.price)
                return True
            except:
                return False
        return True




class SubscriptionManager(models.Manager):
    def custom_create(self, package, user, flights):
        try:
            # Create a subscription
            with transaction.atomic():
                
                # Create reservations and set first_flight_date and last_flight_date
                first_flight_date = None
                last_flight_date = None
                reservations = []

                for flight in flights:
                    reservations.append(reservation)
                    reservation = Reservation.objects.create(user=user, flight=flight, subscription=subscription)

                    if not first_flight_date or flight.date < first_flight_date:
                        first_flight_date = flight.date
                    if not last_flight_date or flight.date > last_flight_date:
                        last_flight_date = flight.date

                subscription = self.create(package=package, user=user)
                subscription.first_flight_date = first_flight_date
                subscription.last_flight_date = last_flight_date
                subscription.reservations.set(reservations)
                
                subscription.user.deduct_credits(subscription.package.price)
        except Exception:
            return False, reservations[-1]

        return True, subscription




class Subscription(models.Model):
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    first_flight_date = models.DateField(null=True, blank=True)
    last_flight_date = models.DateField(null=True, blank=True)
    reservations= models.ManyToManyField(Reservation)
    
    objects = SubscriptionManager()
    
    def get_passed_reservations(self):
        return self.reservations.count()