import uuid
from django.db import models


class Address(models.Model):
    class Meta:
        ordering = ["id"]
        
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=3)
    complement = models.CharField(max_length=100, null=True)
