from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=3)
    complement = models.CharField(max_length=100, null=True)
