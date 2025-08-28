from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import TravelOption, Booking
from decimal import Decimal
from datetime import timedelta

class BookingFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.travel = TravelOption.objects.create(
            travel_id="TR001",
            type="BUS",
            source="CityA",
            destination="CityB",
            departure_datetime=timezone.now() + timedelta(days=1),
            price=Decimal('100.00'),
            available_seats=10
        )

    def test_booking_reduces_seats(self):
        self.client.login(username='alice', password='pass123')
        resp = self.client.post(f"/travel/{self.travel.pk}/book/", {"number_of_seats": 2})
        self.assertEqual(resp.status_code, 302)
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 8)
        self.assertEqual(Booking.objects.count(), 1)

    def test_cannot_overbook(self):
        self.client.login(username='alice', password='pass123')
        resp = self.client.post(f"/travel/{self.travel.pk}/book/", {"number_of_seats": 999})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Not enough seats available.")
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 10)
