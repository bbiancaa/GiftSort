from django import forms
from raffle.models import Room, Participant, CategoryGift


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'min_value', 'max_value')


class ParticipantForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=CategoryGift.objects.all(), 
        widget=forms.Select(attrs={'class': 'custom-select custom-select'}),
        empty_label='Selecione'
        )
    obs = forms.CharField(required=False, widget=forms.Textarea())
    class Meta:
        model = Participant
        fields = ('name', 'email', 'category', 'obs')