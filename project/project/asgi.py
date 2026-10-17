"""
ASGI configiration for project project.

It exposess the ASGI callable as a module-level variable named ``applicetion``.


"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_asgi_application()
