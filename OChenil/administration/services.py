from administration.models import Dog, Booking, Box, Unavailability, Size
from administration.forms import AllBookingsForm, AllBoxForm
from authentication.models import User
from customer.forms import DogForm, BookingForm
from datetime import date, timedelta, datetime
from generic.constants import (NBR_DAYS_CAPACITY,
                               IMPOSSIBLE_UNAVAILABILITY,
                               UNAVAILABILITY_OK,
                               BOOKING_DELETION_OK,
                               BOOKING_NOT_DELETED)
from django.urls import resolve
from generic.custom_logging import custom_log


class Services():
    def __init__(self):
        pass

    def list_bookings(self):
        """returns all the bookings from all users"""
        return Booking.objects.all()

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
                # custom_log("capacity", capacity)
            daily_capacity.append([date_start, capacity])
            # custom_log("daily_capacity", daily_capacity)
            date_start = date_start+timedelta(days=1)
        return daily_capacity

    def action_if_POST(self, request):
        """call the required functions if admin user request to cancel a
        booking or declare an unavailability"""
        message = ''
        message_type = 'success'
        booking_list_form = AllBookingsForm()
        box_list_form = AllBoxForm()
        if request.method == "POST":
            required_action = request.POST.get('required_action')
            custom_log("required_action", required_action)
            # custom_log("required_action", required_action)
            if required_action == "cancel_booking":
                cancel = self.cancel_booking(request)
                message = cancel[0]
                message_type = cancel[1]
            if required_action == "unavailability":
                unavailability = self.create_unavailability(request)
                message = unavailability[0]
                custom_log("message unavailability", message)
                message_type = unavailability[1]
        return booking_list_form, box_list_form, message, message_type

    def cancel_booking(self, request):
        """Cancel booking based on an id selected by an admin user

        Returns:
        booking objects (all bookings)"""
        id_to_be_canceled = request.POST['id_to_be_canceled']
        booking_to_be_canceled = Booking.objects.get(
            pk=id_to_be_canceled)
        booking_to_be_canceled.delete()
        ids_remaining_bookings = Booking.objects.all().values_list('id', flat=True)
        custom_log("ids_remaining_bookings", ids_remaining_bookings)
        if id_to_be_canceled in ids_remaining_bookings:
            message = BOOKING_NOT_DELETED
            message_type = 'warning'
        elif id_to_be_canceled not in ids_remaining_bookings:
            message = BOOKING_DELETION_OK
            message_type = 'success'
        return message, message_type

    def create_unavailability(self, request):
        """Create an unavailability based on information entered 
        by an admin user in the managemenet.html page"""
        id_box_unavailable = request.POST['id_box']
        s_date_year = int(request.POST['start_year'])
        s_date_month = int(request.POST['start_month'])
        s_date_day = int(request.POST['start_day'])
        unavailability_start = datetime(
            s_date_year, s_date_month, s_date_day)
        e_date_year = int(request.POST['end_year'])
        e_date_month = int(request.POST['end_month'])
        e_date_day = int(request.POST['end_day'])
        unavailability_end = datetime(
            e_date_year, e_date_month, e_date_day)
        box_unavailable = Box.objects.get(pk=id_box_unavailable)
        check_if_booked = Booking.objects.filter(
            box=id_box_unavailable,
            start_date__lte=unavailability_end,
            end_date__gte=unavailability_start).first()
        custom_log("check_if_booked", check_if_booked)
        if check_if_booked:
            message = IMPOSSIBLE_UNAVAILABILITY
            message_type = 'warning'
        else:
            unavailable = Unavailability(start_date=unavailability_start,
                                         end_date=unavailability_end,
                                         box=box_unavailable)
            unavailable.save()
            unavailable.refresh_from_db()
            message = UNAVAILABILITY_OK
            message_type = 'success'
        return message, message_type
