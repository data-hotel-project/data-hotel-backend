from django.db import models

from address.models import Address
from customUser.models import CustomUser


class Guest(CustomUser):
    address = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, null=True, blank=True
    )

    class Meta:
        ordering = ["id"]
