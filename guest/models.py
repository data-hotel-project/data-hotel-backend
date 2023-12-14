from django.db import models

from address.models import Address
from customUser.models import CustomUser


class Guest(CustomUser):
    class Meta:
        ordering = ["created_at"]

    address = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, null=True, blank=True
    )
