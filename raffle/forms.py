from django import forms
from raffle.models import Room, Participant, CategoryGift


class RoomForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        min_value = cleaned_data.get('min_value')
        max_value = cleaned_data.get('max_value')
        if max_value and min_value:
            if max_value < min_value:
                self.add_error('min_value', "Valor mínimo não pode ser maior que o valor máximo")

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
    link_short = forms.CharField(max_length=50, required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        link_short = cleaned_data.get('link_short')
        if Room.objects.filter(participant__email=email, link=link_short).exists():
            self.add_error('email', "Esse email já está participando nesse sorteio")

    class Meta:
        model = Participant
        fields = ('name', 'email', 'category', 'obs', 'link_short')
