import uuid
from django.db import models
from guest.models import Guest


class Reservation(models.Model):
    class Meta:
        ordering = ["id"]
        
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    quantity = models.PositiveIntegerField()
    entry_date = models.DateTimeField()
    departure_date = models.DateTimeField()

    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name="reservations"
    )
