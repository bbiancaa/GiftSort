
from django.urls import path, include
from raffle.views import HomeView, CreateRoomView, CreateParticipantView, DetailRoomView


urlpatterns = [
    path('', HomeView.as_view()),
    path('criar-sala', CreateRoomView.as_view(), name='criar-sala'),
    path('detalhe-sala/<int:pk>/', DetailRoomView.as_view(), name='detalhe-sala'),
    path('criar-participante', CreateParticipantView.as_view(), name='criar-participante'),
]