from django import forms

SIZE_CHOICES = [
    ('petit', 'petit'),
    ('grand', 'grand'),
]


class DogForm(forms.Form):
    dog_name = forms.CharField(required=True)
    dog_age = forms.IntegerField(required=True)
    dog_size = forms.IntegerField(widget=forms.Select(choices=SIZE_CHOICES))
    dog_race = forms.CharField(required=True)
