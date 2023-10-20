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
        self.program = Program.objects.create(govern=self.govern, move_from=self.move_from_area, move_to=self.move_to_area, bus=self.bus, duration='2 hours', price=50)
        self.program.move_at.add(self.appointment)
        
        self.flight = Flight.objects.create(program=self.program, date='2023-10-30')

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

    # Write more test cases for different scenarios, e.g., trying to reserve a seat on a full flight.

# You can write additional test cases as needed to cover different scenarios.
