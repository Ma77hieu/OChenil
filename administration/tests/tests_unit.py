from administration.services import Services
from django.http import HttpRequest
from administration.models import Booking, Unavailability
from generic.constants import BOOKING_DELETION_OK, UNAVAILABILITY_OK
from generic.custom_logging import custom_log
from django.test import TestCase


class UnitTest(TestCase):
    fixtures = ['fixture_db.json']

    def test_list_booking(self):
        ids_bookings_test_db = list(
            Booking.objects.all().values_list('id', flat=True))
        # custom_log("ids_bookings_test_db", ids_bookings_test_db)
        list_bookings = Services.list_bookings(self)
        ids = list(list_bookings.values_list('id', flat=True))
        # custom_log("ids", ids)
        assert ids == ids_bookings_test_db

    def test_cancel_booking(self):
        request = HttpRequest()
        ids_bookings_test_db = list(
            Booking.objects.all().values_list('id', flat=True))
        # custom_log("ids_bookings_test_db", ids_bookings_test_db)
        request.POST['id_to_be_canceled'] = ids_bookings_test_db[0]
        message = Services.cancel_booking(self, request)[0]
        # custom_log("message", message)
        assert message == BOOKING_DELETION_OK

    def test_create_unavailability(self):
        request = HttpRequest()
        request.POST['id_box'] = 1
        request.POST['start_year'] = 2023
        request.POST['start_month'] = 8
        request.POST['start_day'] = 1
        request.POST['end_year'] = 2023
        request.POST['end_month'] = 8
        request.POST['end_day'] = 2
        unavailability = Services.create_unavailability(self, request)[0]
        assert unavailability == UNAVAILABILITY_OK
