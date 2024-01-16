import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    birthdate = models.DateField(null=True)
    nationality = models.CharField(max_length=20)
    contact = models.CharField(max_length=50)
    aditional_contact = models.CharField(max_length=11, blank=True, default="")
    emergency_num = models.CharField(max_length=11)
    email = models.EmailField(max_length=50, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
