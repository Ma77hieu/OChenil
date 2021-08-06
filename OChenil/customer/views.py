from django.shortcuts import render
from customer.services import Services

# Create your views here.


def user(request):
    """view managing the acess to the user's account"""
    dogs_info = Services().dog_management(request)
    dog_form = dogs_info[0]
    user_feedback = dogs_info[1]
    context = ({'form': dog_form, 'user_feedback': user_feedback})
    return render(request, 'user.html', context)
