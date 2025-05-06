# konnaxion_project/config/settings/local.py

import os
import environ
from .base import *

# Initialize environment variables
env = environ.Env(DEBUG=(bool, False))
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR, "..", ".envs", ".local", ".django")
environ.Env.read_env(env_file)

DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": env.db(),  # Expects DATABASE_URL in your .env file
}

# Static and media settings
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Additional settings can be added as needed
from .base import *  # Import base settings

# Debug Toolbar

import sys

if DEBUG and "test" not in sys.argv:  # ✅ Only add Debug Toolbar in development mode
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


# Show Debug Toolbar only in development mode
INTERNAL_IPS = [
    "127.0.0.1",  # Enable for local development
]

# If using Docker, add this to ensure the toolbar works inside containers:
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [ip[: ip.rfind(".")] + ".1" for ip in ips]

# Forcer l'affichage de la Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {
#    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    "IS_RUNNING_TESTS": False,
}