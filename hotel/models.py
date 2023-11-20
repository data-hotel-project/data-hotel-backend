import uuid
from django.db import models
from cloudinary.models import CloudinaryField


class Hotel(models.Model):
    class Meta:
        ordering = ["id"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    num_rooms = models.PositiveIntegerField()
    image = CloudinaryField("image")

    address = models.OneToOneField("address.Address", on_delete=models.DO_NOTHING)
