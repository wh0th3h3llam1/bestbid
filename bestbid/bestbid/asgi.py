from channels.routing import get_default_application
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bestbid.settings")
django.setup()

application = get_default_application()
