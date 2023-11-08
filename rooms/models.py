from django.db import models


class RoomStatusChoice(models.TextChoices):
    FREE = "Free"
    OCCUPIED = "Occupied"
    CLEANING = "Cleaning"
    MAINTENANCE = "Under maintenance"


class Rooms(models.Model):
    number = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=18, choices=RoomStatusChoice.choices, default=RoomStatusChoice.FREE
    )
    entry_date = models.DateTimeField()


# Create your models here.
