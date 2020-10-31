from django.conf import settings
from django.db.models import signals
from django.utils.importlib import import_module
from imp import find_module
from os import environ




def apply_patches():
    """
    Import `patches` from all the `INSTALLED_APPS`
    """

    for app in settings.INSTALLED_APPS:
        try:
            app_path = import_module(app).__path__
            
        except AttributeError:
            continue

        try:
            find_module('patches', app_path)
        except ImportError:
            continue

        import_module('%s.patches' % app)

if environ['DJANGO_SETTINGS_MODULE'].startswith('appsphere.'):
    # DJANGO_UPGRADE: Stop patching.
    # apply_patches()
    pass
