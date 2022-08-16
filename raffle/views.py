import random
import string

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView

from raffle.forms import RoomForm, ParticipantForm
from raffle.models import Room, Participant, RaffleParticipant


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
    success_message = "Agora você já está participando do Amigo Secreto, link para compartilhar a sala: \n%(link)s" \
                      "\n\nId da sala:\n%(room_id)s\nGuarde pois vai precisar para fazer o sorteio!"

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
            link=self.request.build_absolute_uri(Room.objects.get(room_id=self.kwargs.get('room_id')).link),
            room_id=self.kwargs.get('room_id')
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

    def get_context_data(self, **kwargs):
        context = super(CreateParticipanteShortView, self).get_context_data(**kwargs)
        context['link_short'] = self.kwargs.get('link_short')
        return context

    def form_valid(self, form):
        participant = form.save(commit=False)
        participant.save()
        room = Room.objects.get(link=self.kwargs.get('link_short'))
        if room.is_locked:
            messages.error(self.request, "Sala não permite novos participantes", extra_tags="danger")
            participant.delete()
            return redirect(self.success_url)
        room.participant.add(participant)
        return super().form_valid(form)


class UpdateParticipanteView(SuccessMessageMixin, UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'raffle/editar_participante.html'
    success_message = "Cadastro editado com sucesso"
    success_url = '/'

    def get_object(self):
        return Participant.objects.get(id=self.request.GET['participant_id'])


class UpdateRoomView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'raffle/editar_sala.html'
    success_message = "Sala editada com sucesso"
    success_url = '/'

    def get_object(self):
        return Room.objects.get(room_id=self.request.GET['room_id'])

    def post(self, request, *args, **kwargs):
            if self.get_object().is_locked:
                messages.error(self.request, "Sala não pode ser atualizada\nSorteio já realizado", extra_tags="danger")
            else:
                messages.success(self.request, self.success_message)
            return super(UpdateRoomView, self).post(request, args, kwargs)


class DetailRoomForRaffleView(DetailView):
    model = Room
    template_name = 'raffle/detalhe_sala.html'
    form_class = RoomForm

    def get_object(self):
        return Room.objects.get(room_id=self.request.GET['room_id'])

    def get_context_data(self, **kwargs):
        context = super(DetailRoomForRaffleView, self).get_context_data(**kwargs)
        context['raffle_participants'] = RaffleParticipant.objects.filter(room=self.object)
        context['link_short'] = self.request.get_host() + reverse('criar-participante',
                                                                  kwargs={'link_short': self.get_object().link})
        return context


class ApplyRaffle(View):
    def post(self, request, *args, **kwargs):
        room_id = request.POST.get('room_id')
        room = Room.objects.get(room_id=room_id)
        if room.participant.count() < 2:
            messages.error(self.request, "Sala precisa ter mais participantes", extra_tags="danger")
            return redirect(f"{reverse('detalhe-sortear-sala')}?room_id={room_id}")
        participants = list(room.participant.all().values_list('id', flat=True))
        random.shuffle(participants)
        for i in range(len(participants)):
            RaffleParticipant.objects.get_or_create(
                participant_id=participants[i],
                selected_participant_id=participants[(i + 1) % (len(participants))],
                room=room)
        room.is_locked = True
        room.save()
        messages.success(request, "Sorteio realizado com sucesso!")
        return redirect(f"{reverse('detalhe-sortear-sala')}?room_id={room_id}")


class DetailRaffleUser(DetailView):
    model = RaffleParticipant
    template_name = 'raffle/detalhe_sorteio_sala.html'

    def get_object(self, queryset=None):
        try:
            raffle_participant = RaffleParticipant.objects.filter(participant_id=self.request.GET.get('participant_id'))
        except:
            raffle_participant = RaffleParticipant.objects.filter(
                participant__email=self.request.GET.get('participant_id'))
        if raffle_participant.exists():
            return raffle_participant.first()
        messages.error(self.request, "Nenhum participante encontrado com essas informações.", extra_tags="danger")

    def get(self, request):
        self.object = self.get_object()
        if not self.object:
            return redirect('home')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
