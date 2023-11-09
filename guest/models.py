import uuid
from django.db import models
from address.models import Address


class Guest(models.Model):
    class Meta:
        ordering = ["id"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    birthdate = models.DateTimeField(null=True)
    nationality = models.CharField(max_length=20)
    contact = models.CharField(max_length=50)
    contact_aditional = models.CharField(max_length=11, blank=True, default="")
    emergency_num = models.CharField(max_length=11)

    address = models.OneToOneField(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
