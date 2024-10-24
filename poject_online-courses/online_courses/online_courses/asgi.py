"""
ASGI config for online_courses project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from django.apps import AppConfig

class CoursesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'

    def ready(self):
        import courses.signals  


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_courses.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
})

