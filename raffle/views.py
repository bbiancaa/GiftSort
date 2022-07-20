from django.views.generic import TemplateView, CreateView, DetailView
from raffle.models import Room, Participant
from raffle.forms import RoomForm, ParticipantForm
from django.contrib.messages.views import SuccessMessageMixin

class HomeView(TemplateView):
    template_name = "index.html"


class CreateRoomView(CreateView):
    model = Room
    template_name = 'raffle/criar_sala.html'
    form_class = RoomForm


class CreateParticipantView(SuccessMessageMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'raffle/criar_participante.html'
    success_url = '/'
    success_message = "Agora você já está participando do Amigo Secreto"

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.save()
        room = Room.objects.get(room_id=self.kwargs.get('room_id'))
        room.participant.add(participant)
        # messages.success(self.request, 'Você já está participando do Amigo Secredo.')
        return super().form_valid(form)


class DetailRoomView(DetailView):
    model = Room
    template_name = 'raffle/detalhe_sala.html'
    form_class = RoomForm
