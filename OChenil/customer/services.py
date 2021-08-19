from administration.models import Dog, Booking, Box, Unavailability, Size
from authentication.models import User
from customer.forms import DogForm, BookingForm
from generic.constants import (DOG_ADDED,
                               FAIL_DOG_ADDED,
                               NEED_LOGIN,
                               NO_AVAILABILITY,
                               BOOKING_OK)
from django.urls import resolve
import logging


class Services():
    def __init__(self):
        pass

    def dog_management(self, request):
        """retrieve all the information about the dogs of the user"""
        current_url = resolve(request.path_info).url_name
        if ("signin" in current_url) or request.method == "GET":
            message = ''
            dog_form = DogForm()
        if (not ("signin" in current_url)) and request.method == "POST":
            if not request.user.id:
                message = NEED_LOGIN
            elif request.user.id:
                d_owner = User.objects.get(pk=request.user.id)
                d_name = request.POST['dog_name']
                d_age = request.POST['dog_age']
                d_size = Size.objects.get(pk=request.POST['dogsize'])
                d_race = request.POST['dog_race']
                new_dog = Dog(dog_name=d_name,
                              dog_age=d_age,
                              dogsize=d_size,
                              dog_race=d_race,
                              owner=d_owner)
                new_dog.save()
                message = DOG_ADDED
            dog_form = DogForm()

        return (dog_form, message)

    def list_dogs(self, request):
        """returns all the dogs objects linked to the user"""
        if not request.user.id:
            pass
        elif request.user.id:
            d_owner = User.objects.get(pk=request.user.id)
            dogs = Dog.objects.filter(owner=d_owner)
        return dogs

    def list_bookings(self, request):
        """returns all the bookings linked to the user"""
        if not request.user.id:
            pass
        elif request.user.id:
            d_owner = User.objects.get(pk=request.user.id)
            bookings = Booking.objects.filter(user=d_owner)
        return bookings

    def make_booking(self, request):
        """create a new booking entry in the database after checking for availability"""
        if not request.user.id:
            message = NEED_LOGIN
            html_page = "signin.html"
        else:
            d_owner = User.objects.get(pk=request.user.id)
            if request.method == "GET":
                message = ''
                html_page = "booking.html"
            elif request.method == "POST":
                s_date = request.POST['start_date']
                e_date = request.POST['end_date']
                selected_dog_id = request.POST['dog_name']
                selected_dog = Dog.objects.get(
                    pk=selected_dog_id)
                availability = self.search_availability(
                    selected_dog, s_date, e_date)
                if availability:
                    self.create_booking(
                        selected_dog, d_owner, s_date, e_date, availability)
                    message = BOOKING_OK
                else:
                    message = NO_AVAILABILITY
                    html_page = "booking.html"
            booking_form = BookingForm(request=request)
        return (booking_form, message)

    def create_booking(self, selected_dog, owner, entry_date, exit_date, box_id):
        """create anew instance of Booking model"""
        new_booking = Booking(
            start_date=entry_date,
            end_date=exit_date,
            status="OK",
            user=owner,
            dog=selected_dog,
            box=box_id,
            booking_size=selected_dog.dogsize)
        new_booking.save()

    def search_availability(self, dog, entry_date, exit_date):
        """make sure there is a box with the right size at the requested dates"""
        size = dog.dogsize
        # get all boxes with right size
        good_size_boxes = Box.objects.filter(box_size=size)
        # get all bookings with righht size
        all_bookings_required_size = Booking.objects.filter(booking_size=size)
        # get all bookings with right size at those date + matching boxes
        same_date_and_size_bookings = all_bookings_required_size.filter(
            start_date__lt=exit_date,
            end_date__gt=entry_date
        )
        # booked_good_size_boxes = same_date_and_size_bookings.box.id
        # list of the id of all booked boxes
        ids_booked_good_size_boxes = list(same_date_and_size_bookings.values_list(
            'box', flat=True))
        # get all unavailability with right size
        ids_unavailable_good_size_boxes = []
        if Unavailability.objects.all():
            unavailability_good_size_boxes = Unavailability.objects.filter(
                box__in=good_size_boxes)
            unavailable_good_size_boxes_id = unavailability_good_size_boxes.values_list(
                'id', flat=True)
            # get all bookings with right size at those date + matching boxes
            same_date_and_size_unavailable = Unavailability.objects.filter(
                pk__in=unavailable_good_size_boxes_id,
                start_date__lt=exit_date,
                end_date__gt=entry_date
            )
            # unavailable_good_size_boxes = same_date_and_size_unavailable.box
            # list of the id of all unavailable boxes
            if same_date_and_size_unavailable:
                ids_unavailable_good_size_boxes = list(same_date_and_size_unavailable.values_list(
                    'box', flat=True))
        # list of the id of all not good size boxes
        ids_bad_size_boxes = list(Box.objects.exclude(
            box_size=size).values_list('id', flat=True))
        # list of the id of all not suitable boxes
        ids_not_suitable_box = (ids_bad_size_boxes
                                + ids_unavailable_good_size_boxes
                                + ids_booked_good_size_boxes)
        # get one right size boox not booked or unavailable
        available_box = Box.objects.exclude(pk__in=ids_not_suitable_box)
        if available_box:
            one_available_box = available_box.first()
            return one_available_box
        else:
            return False
