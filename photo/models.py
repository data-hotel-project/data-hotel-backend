from django.db import models
from hotel.models import Hotel
from room.models import Room


class Photo(models.Model):
    file = models.ImageField(upload_to="img")

    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="hotel_imgs", null=True
    )

    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room_imgs", null=True
    )
