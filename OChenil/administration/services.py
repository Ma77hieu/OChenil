from administration.models import Dog, Booking, Box, Unavailability, Size
from authentication.models import User
from customer.forms import DogForm, BookingForm
from datetime import date
from datetime import timedelta
from generic.constants import (BOOKING_NOT_DELETED, BOOKING_DELETION_OK)
from django.urls import resolve
import logging


class Services():
    def __init__(self):
        pass

    def list_bookings(self):
        """returns all the bookings from all users"""
        bookings = Booking.objects.all()
        logger = logging.getLogger(__name__)
        logger.error('####################### BBOKINGS')
        logger.error(bookings)

        return bookings

    # def cancel_booking(self, id_booking):
    #     booking_to_delete = Booking.objects.filter(pk=id_booking)
    #     booking_to_delete.delete()
    #     delete_issue = booking_to_delete
    #     if delete_issue:
    #         return BOOKING_NOT_DELETED
    #     else:
    #         return BOOKING_DELETION_OK

    # def daily_capacity(self):
    #     today = date.today()
    #     daily_capacity = []
    #     date_start = today+timedelta(days=-5)
    #     date_end = today+timedelta(days=5)
    #     # for day in range(date_start, date_end):
    #     while date_start <= date_end:
    #         boxes_nbr = Box.objects.all().count()
    #         nbr_bookings = Booking.objects.filter(
    #             start_date__lte=today,
    #             end_date__gt=today).count()
    #         capacity = (date_start, boxes_nbr-nbr_bookings)
    #         daily_capacity.append(capacity)
    #         date_start = date_start+timedelta(days=1)
    #     return daily_capacity
