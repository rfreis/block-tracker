"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


SETTINGS_MODULE_PATH = os.environ.get("SETTINGS_MODULE_PATH", "app.settings.local")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE_PATH)

application = get_asgi_application()
