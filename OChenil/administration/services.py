from administration.models import Dog, Booking, Box, Unavailability, Size
from administration.forms import AllBookingsForm, AllBoxForm
from authentication.models import User
from customer.forms import DogForm, BookingForm
from datetime import date
from datetime import timedelta
from generic.constants import (NBR_DAYS_CAPACITY)
from django.urls import resolve
from generic.custom_logging import custom_log


class Services():
    def __init__(self):
        pass

    def list_bookings(self):
        """returns all the bookings from all users"""
        bookings = Booking.objects.all()
        return bookings

    def daily_capacity(self):
        """calculates the total amount of boxes, the daily nbr of bookings
        the daily box unavailability and remaining daily spots.

        Returns:
        [
            [date],
            [nbr box S,nbr booking S, nbr unavailability S, remaining box S,
            nbr box B,nbr booking B, nbr unavailability B, remaining box B]
        ]
        in the above table, S stands for small dogs and B stand for big dogs
        for each day within today +/-NBR_DAYS_CAPACITY
        """
        today = date.today()
        date_start = today+timedelta(days=-NBR_DAYS_CAPACITY)
        date_end = today+timedelta(days=NBR_DAYS_CAPACITY)
        daily_capacity = []
        while date_start <= date_end:
            capacity = []
            for size in [1, 2]:
                nbr_unavailability = 0
                boxes_right_size = Box.objects.filter(box_size=size)
                boxes_nbr = boxes_right_size.count()
                nbr_bookings = Booking.objects.filter(
                    start_date__lte=date_start,
                    end_date__gte=date_start,
                    booking_size=size).count()
                for box_right_size in boxes_right_size:
                    unavailability = Unavailability.objects.filter(
                        start_date__lte=date_start,
                        end_date__gte=date_start,
                        box=box_right_size)
                    if unavailability:
                        nbr_unavailability += 1
                remain_available = boxes_nbr-nbr_bookings-nbr_unavailability
                all_infos = (boxes_nbr,
                             nbr_bookings, nbr_unavailability, remain_available)
                capacity.extend(all_infos)
                custom_log("capacity", capacity)
            daily_capacity.append([date_start, capacity])
            custom_log("daily_capacity", daily_capacity)
            date_start = date_start+timedelta(days=1)
        return daily_capacity

    def cancel_booking(self, request):
        """Cancel booking based on an id selected by an admin user

        Returns:
        booking objects (all bookings)"""
        if request.method == "POST":
            required_action = request.POST.get('required_action')
            # custom_log("required_action", required_action)
            if required_action == "cancel_booking":
                id_to_be_canceled = request.POST['id_to_be_canceled']
                booking_to_be_canceled = Booking.objects.get(
                    pk=id_to_be_canceled)
                booking_to_be_canceled.delete()
        booking_list_form = AllBookingsForm()
        return booking_list_form

    def create_unavailability(self, request):
        """Create an unavailability based on information entered 
        by an admin user in the managemenet.html page"""
        if request.method == "POST":
            required_action = request.POST.get('required_action')
            # custom_log("required_action", required_action)
            if required_action == "unavailability":
                id_box_unavailable = request.POST['id_box']
                unavailability_start = request.POST['start']
                unavailability_end = request.POST['end']
                box_unavailable = Box.objects.get(pk=id_box_unavailable)
                unavailable = Unavailability(start_date=unavailability_start,
                                             end_date=unavailability_end,
                                             box=box_unavailable)
                unavailable.save()
        box_list_form = AllBoxForm()
        return box_list_form
