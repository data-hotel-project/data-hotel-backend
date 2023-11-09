import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class FunctionChoice(models.TextChoices):
    ADMIN = "Admin"
    RECEPTIONIST = "Receptionist"
    REGULAR = "Regular"


class Employee(AbstractUser):
    class Meta:
        ordering = ["id"]
        
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    birthdate = models.DateField()
    nationality = models.CharField(max_length=20)
    contact = models.CharField(max_length=11)
    contact_aditional = models.CharField(max_length=11, null=True, blank=True)
    emergency_num = models.CharField(max_length=11)
    job_function = models.CharField(
        max_length=20, choices=FunctionChoice.choices, default=FunctionChoice.REGULAR
    )
    admission_date = models.DateTimeField(auto_now_add=True)
    is_working = models.BooleanField(default=True)

    address = models.ForeignKey("address.Address", on_delete=models.DO_NOTHING)

    hotel = models.ForeignKey("hotel.Hotel", on_delete=models.CASCADE)
