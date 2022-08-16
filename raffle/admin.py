from django.contrib import admin
from .models import *


@admin.register(Participant, CategoryGift, Room, RaffleParticipant)
class ParticipantAdmin(admin.ModelAdmin):
    pass
