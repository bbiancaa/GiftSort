from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from raffle.models import Room, Participant
from raffle.forms import RoomForm, ParticipantForm
from django.contrib.messages.views import SuccessMessageMixin
import random
import string

class HomeView(TemplateView):
    template_name = "index.html"


class CreateRoomView(SuccessMessageMixin, CreateView):
    model = Room
    template_name = 'raffle/criar_sala.html'
    form_class = RoomForm

    def form_valid(self, form):
        room = form.save(commit=False)
        room.link = ''.join(random.choice(string.ascii_letters)
                           for x in range(10))
        room.save()
        return super().form_valid(form)


class CreateParticipantView(SuccessMessageMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'raffle/criar_participante.html'
    success_url = '/'
    success_message = "Agora você já está participando do Amigo Secreto, link para compartilhar a sala %(link)s"

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.host = True
        participant.save()
        room = Room.objects.get(room_id=self.kwargs.get('room_id'))
        room.participant.add(participant)
        return super().form_valid(form)
    
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            link=self.request.build_absolute_uri(Room.objects.get(room_id=self.kwargs.get('room_id')).link)
        )


class DetailRoomView(DetailView):
    model = Room
    template_name = 'raffle/detalhe_sala.html'
    form_class = RoomForm


class CreateParticipanteShortView(SuccessMessageMixin, CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'raffle/criar_participante.html'
    success_message = "Agora você já está participando do Amigo Secreto"
    success_url = '/'

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.save()
        room = Room.objects.get(link=self.kwargs.get('link_short'))
        room.participant.add(participant)
        return super().form_valid(form)



class UpdateParticipanteView(SuccessMessageMixin, UpdateView):
    model = Participant
    form_class= ParticipantForm
    template_name = 'raffle/criar_participante.html'
    success_message = "Cadastro editado com sucesso"
    success_url = '/'