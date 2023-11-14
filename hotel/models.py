import uuid
from django.db import models


class Hotel(models.Model):
    class Meta:
        ordering = ["id"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    num_rooms = models.PositiveIntegerField()

    address = models.OneToOneField("address.Address", on_delete=models.DO_NOTHING)
