from django.db import models
import uuid


class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=200, verbose_name='Name of Room')
    link = models.CharField(max_length=200)
