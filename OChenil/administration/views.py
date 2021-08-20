from django.shortcuts import render
from administration.services import Services
from generic.custom_logging import custom_log


# Create your views here.

def management(request):
    booking_list_form = Services().cancel_booking(request)
    box_list_form = Services().create_unavailability(request)
    bookings = Services().list_bookings()
    capacity = Services().daily_capacity()
    context = ({'bookings': bookings, 'capacity': capacity,
               'booking_list_form':  booking_list_form, 'box_list_form':  box_list_form})
    return render(request, 'management.html', context)
