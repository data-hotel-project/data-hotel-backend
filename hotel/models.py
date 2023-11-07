from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True, unique=True)
    password = models.CharField(max_length=50, null=True)

# Create your models here.
