import uuid
from django.db import models
from guest.models import Guest
from hotel.models import Hotel


class Reservation(models.Model):
    class Meta:
        ordering = ["id"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    quantity = models.PositiveIntegerField()
    entry_date = models.DateTimeField()
    departure_date = models.DateTimeField()

    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name="guest_reservations"
    )

    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="hotel_reservations"
    )
