from operator import truediv
from django.db import models
import uuid


class CategoryGift(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(CategoryGift, on_delete=models.CASCADE)
    obs = models.TextField(blank=True, null=True, verbose_name='Observation')
    host = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('participant-detail', kwargs={'pk': self.pk})


class Room(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100, verbose_name='Name of Room', null=False)
    link = models.CharField(max_length=100)
    min_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                    verbose_name='Minimum value')
    max_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                    verbose_name='Maximum value')
    participant = models.ManyToManyField(Participant, blank=True)
    participant_adm = models.ForeignKey(Participant, null=True, on_delete=models.CASCADE, related_name='participant_adm')
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('criar-participante_uuid', kwargs={'room_id': self.room_id})


class RaffleParticipant(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant')
    selected_participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='selected_participant')

    def __str__(self):
        return f'{self.participant} - {self.selected_participant}'
