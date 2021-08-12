from django.db import models
from authentication.models import User

# Create your models here.


class Size(models.Model):
    size_name = models.CharField(max_length=45)

    def __str__(self):
        return self.size_name


class Dog(models.Model):
    dog_name = models.CharField(max_length=45)
    dog_age = models.IntegerField()
    dogsize = models.ForeignKey(Size, on_delete=models.CASCADE, default=2)
    dog_race = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.dog_name


class Box(models.Model):
    box_size = models.ForeignKey(Size, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return str(self.pk)


class Unavailability(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    box = models.ForeignKey(Box, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=45)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    booking_size = models.ForeignKey(Size, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return str(self.pk)
