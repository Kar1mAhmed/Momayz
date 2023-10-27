from django.test import TestCase
from django.db import transaction

from reservations.models import Reservation, Subscription
from flights.models import Flight, Program
from users.models import User
from locations.models import Area, Govern
from flightsInfo.models import Bus, Appointments, Package

from flights.helpers import get_next_30_dates, create_flight

from django.utils import timezone
import pytz



class ReservationPackageTestCase(TestCase):
    def setUp(self):
        self.govern = Govern.objects.create(name='Test Govern')

        self.move_from_area = Area.objects.create(name='From Area', govern=self.govern)
        self.move_to_area = Area.objects.create(name='To Area', govern=self.govern)
        
        self.user = User.objects.create(email='test@example.com',
                                        name='Test User',
                                        username='testuser',
                                        gender='Male',
                                        credits=100,
                                        city=self.move_from_area)

        self.bus = Bus.objects.create(name='Test Bus', seats=10)

        self.appointment1 = Appointments.objects.create(time='12:00:00')
        self.appointment2 = Appointments.objects.create(time='16:00:00')


        self.program1 = Program.objects.create(govern=self.govern, move_from=self.move_from_area,
                                                move_to=self.move_to_area, bus=self.bus,
                                                duration='2 hours', price=25)
        
        self.program2 = Program.objects.create(govern=self.govern, move_from=self.move_to_area,
                                                move_to=self.move_from_area, bus=self.bus,
                                                duration='2 hours', price=25)
        
        self.program1.move_at.add(self.appointment1)
        self.program2.move_at.add(self.appointment2)
        
        self.package = Package.objects.create(price=300, num_of_flights=10, name="Test package")
        
        self._add_flight_for_next_month(self.program1.pk)
        self._add_flight_for_next_month(self.program2.pk)



    def test_book_package(self):
        self.user.credits = 300
        self.user.save()
        
        package = Package.objects.get(pk=1)
        flights = Flight.objects.all()[:8]
        
    
        with transaction.atomic():
            subscription = Subscription.objects.create(user=self.user, package=package)
            for flight in flights:
                Reservation.objects.create(user=self.user, flight=flight, subscription=subscription)
            self.user.deduct_credits(package.price)

        self.user.refresh_from_db()
        
        self.assertEqual(self.user.credits, 0)        
        self.assertEqual(Reservation.objects.all().count(), len(flights))
        
        for flight in flights:
            self.assertEqual(flight.taken_seats, 1)        
    

    def test_book_package_no_enough_credits(self):
        
        #Creating new instance of flights 
        Flight.objects.all().delete()
        Reservation.objects.all().delete()
        self._add_flight_for_next_month(self.program1.pk)
        self._add_flight_for_next_month(self.program2.pk)

        
        self.user.credits = 100
        self.user.save()
        
        package = Package.objects.get(pk=1)
        flights = Flight.objects.all()[:8]
        
        with self.assertRaises(ValueError):
            subscription = Subscription.objects.create(user=self.user, package=package)
            with transaction.atomic():
                self.user.deduct_credits(package.price)                
                for flight in flights:
                    Reservation.objects.create(user=self.user, flight=flight, subscription=subscription)
        
        self.assertEqual(self.user.credits, 100)        
        self.assertEqual(Reservation.objects.all().count(), 0)
        
        for flight in flights:
            self.assertEqual(flight.taken_seats, 0)        
        

    
    def test_book_package_no_enough_seats(self):
        
        #Creating new instance of flights 
        Flight.objects.all().delete()
        Reservation.objects.all().delete()
        self._add_flight_for_next_month(self.program1.pk)
        self._add_flight_for_next_month(self.program2.pk)

        
        self.user.credits = 300
        self.user.save()
        
        package = Package.objects.get(pk=1)
        flights = Flight.objects.all()[:8]
        
        # set one flight to no seats
        full_flight = flights[7]
        full_flight.taken_seats = full_flight.total_seats
        full_flight.save()
        
        with self.assertRaises(ValueError):
            subscription = Subscription.objects.create(user=self.user, package=package)
            with transaction.atomic():
                    for flight in flights:
                        Reservation.objects.create(user=self.user, flight=flight, subscription=subscription)

        self.assertEqual(Reservation.objects.all().count(), 0)

    def _add_flight_for_next_month(self, program_id):
    
        program = Program.objects.get(pk=program_id)
        cairo_timezone = pytz.timezone('Africa/Cairo')
        today_date = timezone.now().astimezone(cairo_timezone).date()
        dates = get_next_30_dates(str(today_date))
        
        for date in dates:
            flights = Flight.objects.filter(program=program, date=date)
            if not flights.exists():
                create_flight(program=program, date=date)
                
        return True