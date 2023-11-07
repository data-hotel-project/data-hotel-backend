from django.db import models


class RoomStatus(models.TextChoices):
    FREE = 'Free'
    OCCUPIED = 'Occupied'
    CLEANING = 'Cleaning'


class Rooms(models.Model):
    number = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    status = models.CharField(max_length=10,)

# Create your models here.
