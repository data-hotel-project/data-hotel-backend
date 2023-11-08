from django.db import models
from hotel.models import Hotel


class BedroomStatusChoice(models.TextChoices):
    FREE = "Free"
    OCCUPIED = "Occupied"
    CLEANING = "Cleaning"
    MAINTENANCE = "Under maintenance"


class Bedroom(models.Model):
    number = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=18,
        choices=BedroomStatusChoice.choices,
        default=BedroomStatusChoice.FREE,
    )
    entry_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    total_value = models.DecimalField(max_digits=15, decimal_places=2)

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bedrooms")
