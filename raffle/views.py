from django.views.generic import TemplateView, CreateView, DetailView
from raffle.models import Room, Participant
from raffle.forms import RoomForm

class HomeView(TemplateView):
    template_name = "index.html"


class CreateRoomView(CreateView):
    model = Room
    template_name = 'raffle/criar_sala.html'
    form_class = RoomForm


class CreateParticipantView(CreateView):
    model = Participant
    template_name = 'raffle/criar_participante.html'
    fields = '__all__'


class DetailRoomView(DetailView):
    model = Room
    template_name = 'raffle/detalhe_sala.html'
    form_class = RoomForm
