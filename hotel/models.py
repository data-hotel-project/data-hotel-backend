from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    num_rooms = models.PositiveIntegerField()
