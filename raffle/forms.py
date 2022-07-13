from django import forms
from raffle.models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'min_value', 'max_value')