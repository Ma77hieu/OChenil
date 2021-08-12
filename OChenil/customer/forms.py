from django import forms
from administration.models import Dog
from authentication.models import User

SIZE_CHOICES = [
    (1, 'petit'),
    (2, 'grand'),
]


class DogForm(forms.Form):
    dog_name = forms.CharField(required=True)
    dog_age = forms.IntegerField(required=True)
    dogsize = forms.IntegerField(widget=forms.Select(choices=SIZE_CHOICES))
    dog_race = forms.CharField(required=True)


class BookingForm(forms.Form):
    dog_name = forms.ChoiceField()
    start_date = forms.DateField()
    end_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(BookingForm, self).__init__(*args, **kwargs)
        d_owner = User.objects.get(pk=self.request.user.id)
        owner_dogs = Dog.objects.filter(owner=d_owner)
        DOG_CHOICES = [(dog.id, dog.dog_name)for dog in owner_dogs]
        self.fields['dog_name'].choices = DOG_CHOICES
