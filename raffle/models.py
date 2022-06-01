from django.db import models
import uuid


class CategoryGift(models.Model):
    name = models.CharField(max_length=200)


class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    category = models.ForeignKey(CategoryGift, on_delete=models.CASCADE)
    obs = models.TextField()
    host = models.BooleanField(default=False)


class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Name of Room')
    link = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    participant = models.ManyToManyField(Participant)
