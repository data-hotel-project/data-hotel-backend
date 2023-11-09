import uuid
from django.db import models
from hotel.models import Hotel
from guest.models import Guest


class RoomStatusChoice(models.TextChoices):
    FREE = "Free"
    OCCUPIED = "Occupied"
    CLEANING = "Cleaning"
    MAINTENANCE = "Under maintenance"


class Room(models.Model):
    class Meta:
        ordering = ["id"]
        
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    number = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=18,
        choices=RoomStatusChoice.choices,
        default=RoomStatusChoice.FREE,
    )
    entry_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    total_value = models.DecimalField(max_digits=15, decimal_places=2)

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    guest = models.ForeignKey(
        Guest, on_delete=models.DO_NOTHING, related_name="rooms", null=True, blank=True
    )
