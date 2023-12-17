from django.urls import path, re_path
from . import consumers
from . import views

websocket_urlpatterns = [re_path(r'^ws/chat/(?P<room_name>\w+)$', consumers.WebSocketConsumer.as_asgi())]

urlpatterns = [re_path(r'^rooms/$', views.Rooms.as_view()),
               re_path(r'^accept_invite/(?P<invitation_id>\w+)/?$', views.AcceptInvitation.as_view()),
               re_path(r'^create_invite/', views.CreateInvitation.as_view()),
               re_path(r'^leave/$', views.LeaveRoom.as_view())]

