from django.test import TestCase
from reservations.models import Reservation
from flights.models import Flight, Program
from users.models import User
from locations.models import Area, Govern
from flightsInfo.models import Bus, Appointments


class ReservationModelTestCase(TestCase):
    def setUp(self):
        # Create a user and a flight for testing
        self.user = User.objects.create(email='test@example.com', name='Test User', username='testuser', gender='Male', credits=100)
        # Create a govern
        self.govern = Govern.objects.create(name='Test Govern')

        # Create areas
        self.move_from_area = Area.objects.create(name='From Area', govern=self.govern)
        self.move_to_area = Area.objects.create(name='To Area', govern=self.govern)

        # Create a bus
        self.bus = Bus.objects.create(name='Test Bus', seats=10)

        # Create an appointment
        self.appointment = Appointments.objects.create(time='12:00:00')

        # Create a program
        self.program1 = Program.objects.create(govern=self.govern, move_from=self.move_from_area,
                                                move_to=self.move_to_area, bus=self.bus,
                                                duration='2 hours', price=50)
        
        self.program1.move_at.add(self.appointment)
        self.flight = Flight.objects.create(program=self.program1, date='2023-10-20')

    def test_create_reservation(self):
        # Save the initial values
        initial_taken_seats = self.flight.taken_seats
        initial_user_credits = self.user.credits
        
        reservation = Reservation.objects.create(user=self.user, flight=self.flight)
        next_expected_seat_number = reservation._get_seat_number(reservation.flight)
        last_seat_number = next_expected_seat_number - 1

        # Retrieve the flight and user instances again to get updated values
        self.flight.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(self.flight.taken_seats, initial_taken_seats + 1)
        self.assertEqual(self.user.credits, initial_user_credits - self.flight.price)

        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.flight, self.flight)
        self.assertEqual(reservation.seat_number, last_seat_number)
        
        
    def test_replace_reservation(self):
        
        flight1 = Flight.objects.create(program=self.program1, date='2023-10-29')
        flight2 = Flight.objects.create(program=self.program1, date='2023-10-30')

        flight1.taken_seats = 5
        flight2.taken_seats = 8
        flight1.save()
        flight2.save()

        initial_user_credits = self.user.credits
        
        reservation = Reservation.objects.create(user=self.user, flight=flight1)
        self.assertEqual(flight1.taken_seats, 6)
        reservation.objects.replace(flight2)
        self.assertEqual(flight1.taken_seats, 9)
        self.assertEqual(flight1.taken_seats, 5)
        self.assertEqual(initial_user_credits, self.user.credits - flight2.price)


