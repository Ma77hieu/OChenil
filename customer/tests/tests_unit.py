from customer.services import Services
from django.http import HttpRequest
from authentication.models import User
from generic.constants import DOG_ADDED, BOOKING_OK, NO_AVAILABILITY
from django.test import TestCase


class UnitTest(TestCase):
    fixtures = ['fixture_db.json']

    def test_dog_management(self):
        """tests the dog management function (dog creation)"""
        request = HttpRequest()
        test_user = User.objects.get(pk=1)
        request.user = test_user
        request.path_info = "/user"
        request.method = "POST"
        request.POST['dog_name'] = "unit_test_dog"
        request.POST['dog_age'] = 4
        request.POST['dogsize'] = 2
        request.POST['dog_race'] = "Carlin"
        message_added_dog = Services().dog_management(request)[1]
        # custom_log("message_added_dog", message_added_dog)
        assert message_added_dog == DOG_ADDED

    def test_list_dogs(self):
        """tests the list_dogs function"""
        request = HttpRequest()
        test_user = User.objects.get(pk=1)
        request.user = test_user
        dogs = Services().list_dogs(request)
        dogs_id = list(dogs.values_list('id', flat=True))
        dogs_id_from_fixture = [8, 9, 10, 11]
        assert dogs_id == dogs_id_from_fixture

    def test_list_bookings(self):
        """tests the list_bookings function"""
        request = HttpRequest()
        test_user = User.objects.get(pk=1)
        request.user = test_user
        bookings = Services().list_bookings(request)
        bookings_id = list(bookings.values_list('id', flat=True))
        bookings_id_from_fixture = [1, 2, 3, 6]
        assert bookings_id == bookings_id_from_fixture

    def test_make_booking_ok(self):
        """tests the make_booking function and by extension the
         'search availability' function.
        Scenario: availability ok
        """
        request = HttpRequest()
        test_user = User.objects.get(pk=1)
        request.user = test_user
        request.method = "POST"
        request.POST['start_date_year'] = 2023
        request.POST['start_date_month'] = 8
        request.POST['start_date_day'] = 1
        request.POST['end_date_year'] = 2023
        request.POST['end_date_month'] = 8
        request.POST['end_date_day'] = 2
        request.POST['dog_name'] = 9
        new_booking_message = Services().make_booking(request)[1]
        assert new_booking_message == BOOKING_OK

    def test_make_booking_not_ok(self):
        """tests the make_booking function and by extension the
         'search availability' function.
        Scenario: availability NOT ok
        """
        request = HttpRequest()
        test_user = User.objects.get(pk=1)
        request.user = test_user
        request.method = "POST"
        request.POST['start_date_year'] = 2021
        request.POST['start_date_month'] = 8
        request.POST['start_date_day'] = 15
        request.POST['end_date_year'] = 2021
        request.POST['end_date_month'] = 8
        request.POST['end_date_day'] = 16
        request.POST['dog_name'] = 9
        new_booking_message = Services().make_booking(request)[1]
        assert new_booking_message == NO_AVAILABILITY
