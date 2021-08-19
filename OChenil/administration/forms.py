from django import forms
from django.forms.widgets import SelectDateWidget
from administration.models import Booking, Box
from datetime import date
from generic.custom_logging import custom_log


class AllBookingsForm(forms.Form):
    """used in management to cancel a booking"""
    id_to_be_canceled = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        """retrieve the ids of all bookings ending today or later"""
        super(AllBookingsForm, self).__init__(*args, **kwargs)
        today = date.today()
        bookings = Booking.objects.filter(end_date__gte=today)
        ID_LIST_TUPLE = [(booking.id, booking.id) for booking in bookings]
        self.fields['id_to_be_canceled'].choices = ID_LIST_TUPLE


class AllBoxForm(forms.Form):
    """used in management to list box to declare unavailability"""
    id_box = forms.ChoiceField()
    start = forms.DateField(widget=SelectDateWidget())
    end = forms.DateField(widget=SelectDateWidget())

    def __init__(self, *args, **kwargs):
        """retrieve the ids of all boxes"""
        super(AllBoxForm, self).__init__(*args, **kwargs)
        boxes = Box.objects.all()
        ID_LIST_TUPLE = [(box.id, box.id) for box in boxes]
        self.fields['id_box'].choices = ID_LIST_TUPLE
