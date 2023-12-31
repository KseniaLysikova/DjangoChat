# mysite/asgi.py
import os

from channels.auth import CookieMiddleware, SessionMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

asgi = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter({
    "http": asgi,
    "websocket": CookieMiddleware(
        SessionMiddleware(URLRouter(chat.routing.websocket_urlpatterns)))
})
