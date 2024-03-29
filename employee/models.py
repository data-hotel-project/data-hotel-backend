from django.db import models

from address.models import Address
from customUser.models import CustomUser
from hotel.models import Hotel


class FunctionChoice(models.TextChoices):
    ADMIN = "Admin"
    RECEPTIONIST = "Receptionist"
    REGULAR = "Regular"


class Employee(CustomUser):
    job_function = models.CharField(
        max_length=20, choices=FunctionChoice.choices, default=FunctionChoice.REGULAR
    )
    admission_date = models.DateTimeField(auto_now_add=True)

    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="employees")

    class Meta:
        ordering = ["id"]
