from django.urls import path, re_path
from . import consumers
from . import views

websocket_urlpatterns = [re_path(r'^ws/chat/(?P<room_name>\w+)$', consumers.WebSocketConsumer.as_asgi())]

urlpatterns = [re_path(r'^rooms/$', views.Rooms.as_view())]
