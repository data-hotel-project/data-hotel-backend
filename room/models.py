import uuid

from cloudinary.models import CloudinaryField
from django.db import models

from guest.models import Guest
from hotel.models import Hotel


class RoomStatusChoice(models.TextChoices):
    FREE = "Free"
    OCCUPIED = "Occupied"
    CLEANING = "Cleaning"
    MAINTENANCE = "Under maintenance"


class Room(models.Model):
    class Meta:
        ordering = ["number"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    number = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=18,
        choices=RoomStatusChoice.choices,
        default=RoomStatusChoice.FREE,
    )
    entry_date = models.DateTimeField(null=True)
    departure_date = models.DateTimeField(null=True)
    daily_rate = models.DecimalField(max_digits=15, decimal_places=2)
    total_value = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, default=0
    )

    image = CloudinaryField("image")

    image2 = CloudinaryField("image", null=True)
    delete_image2 = models.BooleanField(default=False)

    image3 = CloudinaryField("image", null=True)
    delete_image3 = models.BooleanField(default=False)

    image4 = CloudinaryField("image", null=True)
    delete_image4 = models.BooleanField(default=False)

    image5 = CloudinaryField("image", null=True)
    delete_image5 = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")

    guest = models.ForeignKey(
        Guest, on_delete=models.DO_NOTHING, related_name="rooms", null=True, blank=True
    )
