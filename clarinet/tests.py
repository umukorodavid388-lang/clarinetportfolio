from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import BookingRequest


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class BookingCalendarTests(TestCase):
    def test_calendar_shows_booking_date_without_private_contact_details(self):
        BookingRequest.objects.create(
            name="Private Booker",
            email="booker@example.com",
            engagement_type="recital",
            event_date=date(2026, 6, 15),
            venue="Concert Hall",
            message="A private booking enquiry message.",
        )

        response = self.client.get(reverse("calendar"), {"year": 2026, "month": 6})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "June 2026")
        self.assertContains(response, "15")
        self.assertContains(response, "Booked")
        self.assertNotContains(response, "Sign in to manage booking dates")
        self.assertNotContains(response, "Remove date")
        self.assertNotContains(response, "Concert Hall")
        self.assertNotContains(response, "Private Booker")
        self.assertNotContains(response, "booker@example.com")
        self.assertNotContains(response, "private booking enquiry message")

    def test_calendar_does_not_show_bookings_from_other_months_or_without_dates(self):
        BookingRequest.objects.create(
            name="June Booker",
            email="june@example.com",
            event_date=date(2026, 6, 15),
            message="June booking details.",
        )
        BookingRequest.objects.create(
            name="July Booker",
            email="july@example.com",
            engagement_type="masterclass",
            event_date=date(2026, 7, 15),
            message="July booking details.",
        )
        BookingRequest.objects.create(
            name="Undated Booker",
            email="undated@example.com",
            engagement_type="other",
            message="Date to be confirmed.",
        )

        response = self.client.get(reverse("calendar"), {"year": 2026, "month": 6})

        self.assertContains(response, "June 2026")
        self.assertEqual(response.content.count(b'class="calendar-booking"'), 1)

    def test_calendar_rejects_invalid_month(self):
        response = self.client.get(reverse("calendar"), {"year": 2026, "month": 13})

        self.assertEqual(response.status_code, 404)

    def test_admin_action_removes_date_but_keeps_booking_request(self):
        booking = BookingRequest.objects.create(
            name="Booker",
            email="booker@example.com",
            event_date=date(2026, 6, 15),
            message="A booking request to keep.",
        )
        admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(admin_user)

        response = self.client.post(
            reverse("admin:clarinet_bookingrequest_changelist"),
            {
                "action": "remove_calendar_dates",
                "_selected_action": [booking.pk],
            },
        )

        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertIsNone(booking.event_date)
        self.assertTrue(BookingRequest.objects.filter(pk=booking.pk).exists())
        calendar_response = self.client.get(
            reverse("calendar"),
            {"year": 2026, "month": 6},
        )
        self.assertEqual(calendar_response.content.count(b'class="calendar-booking"'), 0)

    def test_staff_can_remove_booking_date_from_calendar_page(self):
        booking = BookingRequest.objects.create(
            name="Booker",
            email="booker@example.com",
            event_date=date(2026, 6, 15),
            message="A booking request to keep.",
        )
        admin_user = get_user_model().objects.create_superuser(
            username="calendar-admin",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(admin_user)

        calendar_response = self.client.get(
            reverse("calendar"),
            {"year": 2026, "month": 6},
        )
        self.assertContains(calendar_response, "Remove date")

        response = self.client.post(
            reverse("remove_calendar_booking_date", args=[booking.pk]),
        )

        self.assertRedirects(response, "/calendar/?year=2026&month=6")
        booking.refresh_from_db()
        self.assertIsNone(booking.event_date)
        self.assertTrue(BookingRequest.objects.filter(pk=booking.pk).exists())
        self.assertEqual(
            self.client.get(reverse("calendar"), {"year": 2026, "month": 6})
            .content.count(b'class="calendar-booking"'),
            0,
        )

    def test_public_visitor_cannot_remove_booking_date(self):
        booking = BookingRequest.objects.create(
            name="Booker",
            email="booker@example.com",
            event_date=date(2026, 6, 15),
            message="A booking request to keep.",
        )

        response = self.client.post(
            reverse("remove_calendar_booking_date", args=[booking.pk]),
        )

        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.event_date, date(2026, 6, 15))
