import os, django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from backend.middlewares.websocket import AuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

import exchange.routing

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddleware(URLRouter(exchange.routing.websocket_urlpatterns)),
    }
)
