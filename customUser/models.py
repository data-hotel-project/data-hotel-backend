import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    birthdate = models.DateField(null=True)
    nationality = models.CharField(max_length=20)
    contact = models.CharField(max_length=50)
    contact_aditional = models.CharField(max_length=11, blank=True, default="")
    emergency_num = models.CharField(max_length=11)
    email = models.EmailField(max_length=50, unique=True, blank=True)
    is_working = models.BooleanField(default=False)

    # class Meta:
    #     abstract = True
