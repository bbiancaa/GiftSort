
from django.urls import path, include
from raffle.views import HomeView, CreateRoomView, CreateParticipantView


urlpatterns = [
    path('', HomeView.as_view()),
    path('criar-sala', CreateRoomView.as_view(), name='criar-sala'),
    path('criar-participante', CreateParticipantView.as_view(), name='criar-participante'),
]