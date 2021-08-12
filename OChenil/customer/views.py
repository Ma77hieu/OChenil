from django.shortcuts import render
from customer.services import Services

# Create your views here.


def user(request):
    """view managing the acess to the user's account"""
    add_dog_section = Services().dog_management(request)
    dog_form = add_dog_section[0]
    user_feedback = add_dog_section[1]
    dogs = Services().list_dogs(request)
    bookings = Services().list_bookings(request)
    context = (
        {'form': dog_form, 'user_feedback': user_feedback, 'dogs': dogs, 'bookings': bookings})
    return render(request, 'user.html', context)


def book_dates(request):
    """view managing the booking page"""
    dogs = Services().list_dogs(request)
    bookings = Services().list_bookings(request)
    availability = Services().make_booking(request)
    user_feedback = availability[1]
    new_booking = availability[0]
    context = (
        {'dogs': dogs, 'bookings': bookings, 'form': new_booking, 'user_feedback': user_feedback})
    return render(request, 'booking.html', context)


def box_choice(request):
    available_box = Services().box_choice(request)
    context = (
        {'user_feedback': available_box})
    return render(request, 'user.html', context)
