import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from address.models import Address


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    birthdate = models.DateTimeField(null=True)
    nationality = models.CharField(max_length=20)
    contact = models.CharField(max_length=50)
    contact_aditional = models.CharField(max_length=11, blank=True, default="")
    emergency_num = models.CharField(max_length=11)
    email = models.EmailField(max_length=50, unique=True)

    class Meta:
        abstract = True


class Guest(CustomUser):
    address = models.OneToOneField(
        Address, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    groups = models.ManyToManyField(Group, related_name="guest_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="guest_user_permissions"
    )

    class Meta:
        ordering = ["id"]
