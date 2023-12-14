import uuid
from django.db import models


class Address(models.Model):
    class Meta:
        ordering = ["created_at"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=3)
    complement = models.CharField(max_length=100, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
