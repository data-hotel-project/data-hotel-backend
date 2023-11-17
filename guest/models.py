from django.db import models

from address.models import Address
from customUser.models import CustomUser


class Guest(CustomUser):
    address = models.OneToOneField(
        Address, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    # groups = models.ManyToManyField(Group, related_name="guest_groups")
    # user_permissions = models.ManyToManyField(
    #     Permission, related_name="guest_user_permissions"
    # )

    class Meta:
        ordering = ["id"]
