
from django.urls import path, include
from raffle.views import *


urlpatterns = [
    path('', HomeView.as_view()),
    path('criar-sala', CreateRoomView.as_view(), name='criar-sala'),
    path('detalhe-sala/<int:pk>/', DetailRoomView.as_view(), name='detalhe-sala'),
    path('criar-participante/<uuid:room_id>', CreateParticipantView.as_view(), name='criar-participante_uuid'),
    path('criar-participante/<str:link_short>', CreateParticipanteShortView.as_view(), name='criar-participante'),
    path('editar-participante/', UpdateParticipanteView.as_view(), name='editar-participante_uuid'),
    path('editar-sala/', UpdateRoomView.as_view(), name='editar-sala_uuid'),
    path('ver-sala/', DetailRoomForRaffleView.as_view(), name='detalhe-sortear-sala'),
    path('fazer-sorteio/', ApplyRaffle.as_view(), name='fazer-sorteio'),
]