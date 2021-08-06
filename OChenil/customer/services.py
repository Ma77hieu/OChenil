from administration.models import Dog, Booking
from authentication.models import User
from customer.forms import DogForm
from generic.constants import DOG_ADDED, FAIL_DOG_ADDED, NEED_LOGIN


class Services():
    def __init__(self):
        pass

    def dog_management(self, request):
        """retrieve all the information about the dogs of the user"""
        if request.method == "POST":
            if not request.user.id:
                message = NEED_LOGIN
            elif request.user.id:
                d_owner = User.objects.get(pk=request.user.id)
                d_name = request.POST['dog_name']
                d_age = request.POST['dog_age']
                d_size = request.POST['dog_size']
                d_race = request.POST['dog_race']
                new_dog = Dog(dog_name=d_name,
                              dog_age=d_age,
                              dog_size=d_size,
                              dog_race=d_race,
                              owner=d_owner)
                new_dog.save()
                message = DOG_ADDED
            dog_form = DogForm()
        if request.method == "GET":
            message = ''
            dog_form = DogForm()
        return (dog_form, message)
