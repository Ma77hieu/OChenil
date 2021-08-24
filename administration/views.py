from django.shortcuts import render
from administration.services import Services


# Create your views here.

def management(request):
    cancel_or_unavailbility = Services().action_if_POST(request)
    bookings = Services().list_bookings()
    capacity = Services().daily_capacity()
    context = ({'bookings': bookings,
                'capacity': capacity,
                'booking_list_form':  cancel_or_unavailbility[0],
                'box_list_form':  cancel_or_unavailbility[1],
                'user_feedback':  cancel_or_unavailbility[2],
                'message_type':  cancel_or_unavailbility[3]})
    return render(request, 'management.html', context)
