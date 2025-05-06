

---
## manage.py

```py
#!/usr/bin/env python
# ruff: noqa
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # Set the default settings module to the local settings.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # Add the current directory (project root) and the 'apps' folder to sys.path.
    current_path = Path(__file__).parent.resolve()
    sys.path.insert(0, str(current_path))
    apps_path = current_path / "apps"
    sys.path.insert(0, str(apps_path))

    execute_from_command_line(sys.argv)

```


---
## config\settings\base.py

```py
# ruff: noqa: ERA001, E501
"""Base settings to build other settings files upon.
\config\settings\base.py

"""

import os
import ssl
from pathlib import Path

import environ

# ------------------------------------------------------------------------------
# PATHS
# ------------------------------------------------------------------------------
# BASE_DIR is three levels up from config/settings/base.py,
# i.e. C:\MonCode\KonnaxionV3
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# APPS_DIR now points to the folder holding our Django apps.
APPS_DIR = BASE_DIR / "apps"

env = environ.Env()

# This flag controls whether to load .env files.
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
#if READ_DOT_ENV_FILE:
    # Loads environment variables from '.envs/.local/.django' relative to BASE_DIR.
env.read_env(os.path.join(BASE_DIR, ".envs", ".local", ".django"))

# ------------------------------------------------------------------------------
# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# ------------------------------------------------------------------------------
# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="konnaxion"),
        "USER": env("POSTGRES_USER", default="konnaxion_user"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="Gr05bo55"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
        "ATOMIC_REQUESTS": True,
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# URLS
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------------------------
# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize",  # Handy template tags
    "django.contrib.admin",
    "django.forms",
    "django_extensions",
]
THIRD_PARTY_APPS = [
    "celery",
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    "webpack_loader",
]

LOCAL_APPS = [
    "common",
    "konnaxion.core",
    "konnaxion.search",
    "konnaxion.ai",
    "konnaxion.notifications",
    "konnaxion.messaging",
    "konnaxion.ekoh",

    "konnected.foundation",
    "konnected.learning",
    "konnected.team",
    "konnected.paths",
    "konnected.konnectedcommunity",
    "konnected.offline",

    "keenkonnect.projects",
    "keenkonnect.gap_analysis",
    "keenkonnect.expert_match",
    "keenkonnect.team_formation",
    "keenkonnect.collab_spaces",
    "keenkonnect.knowledge_hub",

    "ethikos.home",
    "ethikos.debate_arena",
    "ethikos.stats",
    "ethikos.knowledge_base",
    "ethikos.prioritization",
    "ethikos.resolution",

    "kreative.artworks",
    "kreative.marketplace",
    "kreative.kreativecommunity",
    "kreative.immersive",
]



INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ------------------------------------------------------------------------------
# MIGRATIONS
# ------------------------------------------------------------------------------
# MIGRATION_MODULES = {"sites": "contrib.sites.migrations"}

# ------------------------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# Update custom user model to point to our new model in the konnaxion_core app.
AUTH_USER_MODEL = "core.CustomUser"
LOGIN_REDIRECT_URL = "users:redirect"  # Adjust if needed.
LOGIN_URL = "account_login"

# ------------------------------------------------------------------------------
# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# ------------------------------------------------------------------------------
# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"
# Assuming you have a global static folder at BASE_DIR/static.
STATICFILES_DIRS = [str(BASE_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ------------------------------------------------------------------------------
# MEDIA
# ------------------------------------------------------------------------------
MEDIA_ROOT = str(BASE_DIR / "media")
MEDIA_URL = "/media/"

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Using the global templates folder at BASE_DIR/templates.
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [
                "django.templatetags.static",  # Fix for {% static %} errors.
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                # Update or remove this if necessary:
                "users.context_processors.allauth_settings",
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# FORM RENDERER & CRISPY FORMS
# ------------------------------------------------------------------------------
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# ------------------------------------------------------------------------------
# FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (str(BASE_DIR / "fixtures"),)

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# ------------------------------------------------------------------------------
# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_TIMEOUT = 5

# ------------------------------------------------------------------------------
# ADMIN
# ------------------------------------------------------------------------------
ADMIN_URL = "admin/"
ADMINS = [("Réjean McCormick", "boatbuilder610@gmail.com")]
MANAGERS = ADMINS
DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

# ------------------------------------------------------------------------------
# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# ------------------------------------------------------------------------------
# REDIS & CELERY SETTINGS
# ------------------------------------------------------------------------------
REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = env("REDIS_URL", default=env("CELERY_BROKER_URL", default="redis://localhost:6379/0"))
CELERY_RESULT_BACKEND = env("REDIS_URL", default=env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0"))
REDIS_SSL = CELERY_BROKER_URL.startswith("rediss://")
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None
CELERY_REDIS_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 5 * 60  # 5 minutes hard limit
CELERY_TASK_SOFT_TIME_LIMIT = 60   # 1 minute soft limit
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_RABBITMQ_BROKER_URL = env("CELERY_RABBITMQ_BROKER_URL", default="amqp://guest:guest@localhost:5672//")

# ------------------------------------------------------------------------------
# django-allauth SETTINGS
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ADAPTER = "users.adapters.AccountAdapter"
ACCOUNT_FORMS = {"signup": "users.forms.UserSignupForm"}
SOCIALACCOUNT_ADAPTER = "users.adapters.SocialAccountAdapter"
SOCIALACCOUNT_FORMS = {"signup": "users.forms.UserSocialSignupForm"}

# ------------------------------------------------------------------------------
# django-rest-framework SETTINGS
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    # For development only: allow all requests without authentication.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # If you want to keep authentication classes (they won’t block requests if permission is AllowAny)
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    # Optionally, include your schema class if needed:
    # "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# ------------------------------------------------------------------------------
# django-cors-headers SETTINGS
# ------------------------------------------------------------------------------
CORS_URLS_REGEX = r"^/api/.*$"

# Allow your Next.js dev server to talk to Django
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Allow cookies (session authentication)
CORS_ALLOW_CREDENTIALS = True

# ------------------------------------------------------------------------------
# drf-spectacular SETTINGS
# ------------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "Konnaxion API",
    "DESCRIPTION": "Documentation of API endpoints of Konnaxion",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "SCHEMA_PATH_PREFIX": "/api/",
}

# ------------------------------------------------------------------------------
# django-webpack-loader SETTINGS
# ------------------------------------------------------------------------------
WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "STATS_FILE": BASE_DIR / "webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    },
}

# ------------------------------------------------------------------------------
# ASGI & CHANNELS SETTINGS
# ------------------------------------------------------------------------------
ASGI_APPLICATION = "config.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env("REDIS_HOST", default="localhost"), 6379)],
        },
    },
}

# ------------------------------------------------------------------------------
# GRAPHQL (Graphene-Django) SETTINGS
# ------------------------------------------------------------------------------
GRAPHENE = {
    "SCHEMA": "config.schema.schema",
}

# ------------------------------------------------------------------------------
# SENTRY CONFIGURATION
# ------------------------------------------------------------------------------
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env("SENTRY_DSN", default=""),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

# ------------------------------------------------------------------------------
# END OF SETTINGS
# ------------------------------------------------------------------------------

```


---
## config\settings\local.py

```py
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
```


---
## config\settings\production.py

```py
# ruff: noqa: E501
import logging

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .base import *  # noqa: F403
from .base import DATABASES
from .base import INSTALLED_APPS
from .base import REDIS_URL
from .base import SPECTACULAR_SETTINGS
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["okido.wiki"])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicking memcache behavior.
            # https://github.com/jazzband/django-redis#memcached-exceptions-behavior
            "IGNORE_EXCEPTIONS": True,
        },
    },
}

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = "__Secure-sessionid"
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = "__Secure-csrftoken"
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=True,
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF",
    default=True,
)

# STATIC & MEDIA
# ------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Konnaxion <noreply@okido.wiki>",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Konnaxion] ",
)
ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL")

# Anymail
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ["anymail"]
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
# https://anymail.readthedocs.io/en/stable/esps/mailgun/
EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
ANYMAIL = {
    "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
    "MAILGUN_SENDER_DOMAIN": env("MAILGUN_DOMAIN"),
    "MAILGUN_API_URL": env("MAILGUN_API_URL", default="https://api.mailgun.net/v3"),
}


# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        # Errors logged by the SDK itself
        "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
integrations = [
    sentry_logging,
    DjangoIntegration(),
    CeleryIntegration(),
    RedisIntegration(),
]
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    environment=env("SENTRY_ENVIRONMENT", default="production"),
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
)

# django-rest-framework
# -------------------------------------------------------------------------------
# Tools that generate code samples can use SERVERS to point to the correct domain
SPECTACULAR_SETTINGS["SERVERS"] = [
    {"url": "https://okido.wiki", "description": "Production server"},
]
# Your stuff...
# ------------------------------------------------------------------------------

```


---
## config\urls.py

```py
# konnaxion_project/config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from konnaxion.views import debug_test 

# Import API URLs from your custom router
from .api_router import urlpatterns as api_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api_urlpatterns)),  # URLs from api_router.py (no version prefix)
    path('konnaxion/', include('konnaxion.urls')),
    path('keenkonnect/', include('keenkonnect.urls')),
    path('ethikos/', include('ethikos.urls')),
    path('kreative/', include('kreative.urls')),
    path("debug-test/", debug_test, name="debug-test"),
    path('api-auth/', include('rest_framework.urls')),
]

# Include URLs for the sub-applications contained in the "konnected" folder
konnected_patterns = [
    path('foundation/', include('konnected.foundation.urls')),
    path('konnectedcommunity/', include('konnected.konnectedcommunity.urls')),
    path('learning/', include('konnected.learning.urls')),
    path('offline/', include('konnected.offline.urls')),
    path('paths/', include('konnected.paths.urls')),
    path('team/', include('konnected.team.urls')),
]

urlpatterns += [
    path('konnected/', include((konnected_patterns, 'konnected'), namespace='konnected')),
]

# Add Django Debug Toolbar URLs only in development mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

```


---
## pyproject.toml

```toml
# ==== pytest ====
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "--ds=config.settings.test --reuse-db --import-mode=importlib"
python_files = [
    "tests.py",
    "test_*.py",
]

# ==== Coverage ====
[tool.coverage.run]
include = ["konnaxion_project/**"]
omit = ["*/migrations/*", "*/tests/*"]
plugins = ["django_coverage_plugin"]

# ==== mypy ====
[tool.mypy]
python_version = "3.12"
check_untyped_defs = true
ignore_missing_imports = true
warn_unused_ignores = true
warn_redundant_casts = true
warn_unused_configs = true
plugins = [
    "mypy_django_plugin.main",
    "mypy_drf_plugin.main",
]

[[tool.mypy.overrides]]
# Django migrations should not produce any errors:
module = "*.migrations.*"
ignore_errors = true

[tool.django-stubs]
django_settings_module = "config.settings.test"

# ==== djLint ====
[tool.djlint]
blank_line_after_tag = "load,extends"
close_void_tags = true
format_css = true
format_js = true
# TODO: remove T002 when fixed https://github.com/djlint/djLint/issues/687
ignore = "H006,H030,H031,T002"
include = "H017,H035"
indent = 2
max_line_length = 119
profile = "django"

[tool.djlint.css]
indent_size = 2

[tool.djlint.js]
indent_size = 2

[tool.ruff]
target-version = "py312"
# Exclude a variety of commonly ignored directories.
extend-exclude = [
    "*/migrations/*.py",
    "staticfiles/*",
]

[tool.ruff.lint]
select = [
  "F",
  "E",
  "W",
  "C90",
  "I",
  "N",
  "UP",
  "YTT",
  # "ANN", # flake8-annotations: we should support this in the future but 100+ errors atm
  "ASYNC",
  "S",
  "BLE",
  "FBT",
  "B",
  "A",
  "COM",
  "C4",
  "DTZ",
  "T10",
  "DJ",
  "EM",
  "EXE",
  "FA",
  'ISC',
  "ICN",
  "G",
  'INP',
  'PIE',
  "T20",
  'PYI',
  'PT',
  "Q",
  "RSE",
  "RET",
  "SLF",
  "SLOT",
  "SIM",
  "TID",
  "TC",
  "INT",
  # "ARG", # Unused function argument
  "PTH",
  "ERA",
  "PD",
  "PGH",
  "PL",
  "TRY",
  "FLY",
  # "NPY",
  # "AIR",
  "PERF",
  # "FURB",
  # "LOG",
  "RUF",
]
ignore = [
  "S101", # Use of assert detected https://docs.astral.sh/ruff/rules/assert/
  "RUF012", # Mutable class attributes should be annotated with `typing.ClassVar`
  "SIM102", # sometimes it's better to nest
  "UP038", # Checks for uses of isinstance/issubclass that take a tuple
          # of types for comparison.
          # Deactivated because it can make the code slow:
          # https://github.com/astral-sh/ruff/issues/7871
]
# The fixes in extend-unsafe-fixes will require
# provide the `--unsafe-fixes` flag when fixing.
extend-unsafe-fixes = [
    "UP038",
]

[tool.ruff.lint.isort]
force-single-line = true

```


---
## requirements\local.txt

```txt
# -------------------------------
# Core Frameworks & Libraries
# -------------------------------
Django                         # Full-stack web framework
djangorestframework            # REST API support for Django
channels                       # Real-time WebSocket support for Django
celery                         # Asynchronous task processing
redis                          # Redis client (used for caching, Channels, and Celery broker)
psycopg                        # PostgreSQL adapter (optionally use extras for additional features)
drf-spectacular                # OpenAPI schema generation for DRF
django-allauth                 # Comprehensive account management and social logins
djangorestframework-simplejwt  # JWT authentication for DRF
django-otp                   # Two-factor authentication for enhanced security

# -------------------------------
# Monitoring & Process Management
# -------------------------------
sentry-sdk                   # Error tracking and performance monitoring (Sentry)
prometheus_client            # Exposes application metrics for Prometheus
gunicorn                     # WSGI server for deploying Django applications

# -------------------------------
# Development Utilities & Tools
# -------------------------------
Werkzeug[watchdog]           # Utility library (with file-watching support)
ipdb                         # Interactive Python debugger
watchfiles                   # Auto-reload tool for file changes

# -------------------------------
# Testing Tools
# -------------------------------
mypy                         # Static type checker for Python
django-stubs[compatible-mypy]  # Type stubs for Django (compatible with mypy)
pytest                       # Testing framework
pytest-sugar                 # Aesthetic test output for pytest
djangorestframework-stubs    # Type stubs for Django REST Framework

# -------------------------------
# Documentation Tools
# -------------------------------
sphinx                       # Documentation generator
sphinx-autobuild             # Live-reloading for Sphinx documentation

# -------------------------------
# Code Quality & Linting
# -------------------------------
ruff                         # Fast Python linter and code formatter
coverage                     # Code coverage measurement
djlint                       # Linter for Django templates and code
pre-commit                   # Manage pre-commit hooks

# -------------------------------
# Django Testing & Utilities
# -------------------------------
factory-boy                 # Test fixtures for Django (and other Python projects)
django-debug-toolbar         # Debug toolbar for Django projects
django-extensions            # Extra management commands and utilities for Django
django-coverage-plugin       # Integration between Django and coverage.py
pytest-django                # Django plugin for pytest

```


---
## requirements\production.txt

```txt
# PRECAUTION: avoid production dependencies that aren't in development

-r base.txt

gunicorn==20.1.0  # Downgraded from 23.0.0 to match tech stack
psycopg[c]==3.2.4  # https://github.com/psycopg/psycopg
sentry-sdk==2.20.0

# Django Email
# ------------------------------------------------------------------------------
django-anymail[mailgun]==12.0  # https://github.com/anymail/django-anymail

```


---
## Procfile

```
release: python manage.py migrate
web: gunicorn config.asgi:application -k uvicorn_worker.UvicornWorker
worker: REMAP_SIGTERM=SIGQUIT celery -A config.celery_app worker --loglevel=info
beat: REMAP_SIGTERM=SIGQUIT celery -A config.celery_app beat --loglevel=info

```


---
## apps\ethikos\debate_arena\apps.py

```py
from django.apps import AppConfig

class EthikosDebateArenaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ethikos.debate_arena'
    verbose_name = "Ethikos Debate Arena"

```


---
## apps\ethikos\debate_arena\admin.py

```py
# apps/ethikos/debate_arena/admin.py

from django.contrib import admin
from ethikos.debate_arena.models import DebateSession, Argument, VoteRecord

@admin.register(DebateSession)
class DebateSessionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'moderator', 'start_time', 'end_time', 'is_active', 'created_at')
    list_filter = ('is_active', 'moderator')
    search_fields = ('topic', 'description')
    ordering = ('-start_time',)
    
@admin.register(Argument)
class ArgumentAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'debate_session', 'author', 'vote_count', 'created_at')
    list_filter = ('debate_session', 'author')
    search_fields = ('content',)
    ordering = ('-created_at',)

    def short_content(self, obj):
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content
    short_content.short_description = "Argument"

@admin.register(VoteRecord)
class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ('argument', 'voter', 'vote_value', 'timestamp', 'created_at')
    list_filter = ('argument', 'voter')
    ordering = ('-timestamp',)

```


---
## apps\ethikos\debate_arena\models.py

```py
"""
File: apps/ethikos/debate_arena/models.py

Purpose:
Define models for real‑time debate sessions, including threaded arguments,
vote records, and audit trails.
"""

from django.db import models
from common.base_models import BaseModel

class DebateSession(BaseModel):
    """
    Represents a real-time debate session.
    """
    topic = models.CharField(max_length=255, help_text="Title or topic of the debate session")
    description = models.TextField(null=True, blank=True, help_text="Description of the debate session")
    moderator = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="moderated_debates",
        help_text="Moderator of the debate session"
    )
    start_time = models.DateTimeField(help_text="Debate start time")
    end_time = models.DateTimeField(null=True, blank=True, help_text="Debate end time")
    is_active = models.BooleanField(default=True, help_text="Indicates if the debate session is active")

    def __str__(self):
        return self.topic

class Argument(BaseModel):
    """
    Represents an argument within a debate session.
    Supports threaded replies.
    """
    debate_session = models.ForeignKey(
        DebateSession,
        on_delete=models.CASCADE,
        related_name="arguments",
        help_text="Debate session this argument belongs to"
    )
    author = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="arguments",
        help_text="User who posted the argument"
    )
    content = models.TextField(help_text="Content of the argument")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Parent argument for threaded discussions"
    )
    vote_count = models.IntegerField(default=0, help_text="Net vote count for the argument")

    def __str__(self):
        return f"Argument by {self.author} in {self.debate_session.topic}"

class VoteRecord(BaseModel):
    """
    Records a vote on an argument within a debate session.
    """
    argument = models.ForeignKey(
        Argument,
        on_delete=models.CASCADE,
        related_name="vote_records",
        help_text="The argument being voted on"
    )
    voter = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="vote_records",
        help_text="User who cast the vote"
    )
    vote_value = models.IntegerField(help_text="Vote value, e.g., +1 or -1")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the vote was cast")

    def __str__(self):
        return f"Vote by {self.voter} on Argument {self.argument.id}: {self.vote_value}"

```


---
## apps\ethikos\debate_arena\serializers.py

```py
from rest_framework import serializers
from ethikos.debate_arena.models import DebateSession, Argument, VoteRecord

class DebateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateSession
        fields = [
            'id',
            'topic',
            'description',
            'moderator',
            'start_time',
            'end_time',
            'is_active',
            'created_at',
            'updated_at'
        ]

class ArgumentSerializer(serializers.ModelSerializer):
    # Recursively include replies
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Argument
        fields = [
            'id',
            'debate_session',
            'author',
            'content',
            'parent',
            'vote_count',
            'created_at',
            'updated_at',
            'replies'
        ]

    def get_replies(self, obj):
        qs = obj.replies.all()
        return ArgumentSerializer(qs, many=True).data

class VoteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRecord
        fields = [
            'id',
            'argument',
            'voter',
            'vote_value',
            'timestamp',
            'created_at',
            'updated_at'
        ]

```


---
## apps\ethikos\debate_arena\views.py

```py
# apps/ethikos/debate_arena/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ethikos.debate_arena.models import DebateSession, Argument, VoteRecord
from ethikos.debate_arena.serializers import (
    DebateSessionSerializer,
    ArgumentSerializer,
    VoteRecordSerializer
)

logger = logging.getLogger(__name__)


class DebateSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les sessions de débat en temps réel.
    """
    serializer_class = DebateSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'topic']           # à ajuster selon vos champs
    search_fields = ['title', 'description']            # à adapter aux champs de votre modèle
    ordering_fields = ['start_time', 'end_time']
    ordering = ['-start_time']

    def get_queryset(self):
        qs = DebateSession.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "DebateSession queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()       # conserve votre logique de création
        logger.info(
            "DebateSession créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DebateSessionViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def end_session(self, request, pk=None):
        """
        Action pour clôturer une session de débat.
        Met à jour `is_active` et éventuellement `end_time`.
        """
        session = self.get_object()
        try:
            session.is_active = False
            # si end_time est fourni, sinon il reste inchangé
            if 'end_time' in request.data:
                session.end_time = request.data['end_time']
            session.save()
            logger.info(
                "DebateSession (id=%s) clôturée par %s",
                session.pk, request.user
            )
            return Response(
                self.get_serializer(session).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception(
                "Erreur lors de la clôture de la session %s par %s: %s",
                session.pk, request.user, e
            )
            return Response(
                {"detail": "Impossible de clôturer la session."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ArgumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les arguments dans une session de débat.
    """
    serializer_class = ArgumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['session', 'author']             # à ajuster selon vos champs
    search_fields = ['text']                             # à adapter au champ d’argument
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        qs = Argument.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "Argument queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()  # conserve votre logique de création
        logger.info(
            "Argument créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ArgumentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class VoteRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer l'enregistrement des votes sur les arguments.
    """
    serializer_class = VoteRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['argument', 'voter']            # à ajuster selon vos champs
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = VoteRecord.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "VoteRecord queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()  # conserve votre logique de création
        logger.info(
            "VoteRecord créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans VoteRecordViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\ethikos\debate_arena\urls.py

```py
# apps/ethikos/debate_arena/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.debate_arena.views import (
    DebateSessionViewSet,
    ArgumentViewSet,
    VoteRecordViewSet,
)

app_name = "debate_arena"

router = DefaultRouter()
router.register(r"debate_sessions", DebateSessionViewSet, basename="debate-session")
router.register(r"arguments",       ArgumentViewSet,      basename="argument")
router.register(r"vote_records",    VoteRecordViewSet,    basename="voterecord")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\ethikos\debate_arena\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DebateSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "topic",
                    models.CharField(
                        help_text="Title or topic of the debate session", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Description of the debate session",
                        null=True,
                    ),
                ),
                ("start_time", models.DateTimeField(help_text="Debate start time")),
                (
                    "end_time",
                    models.DateTimeField(
                        blank=True, help_text="Debate end time", null=True
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Indicates if the debate session is active",
                    ),
                ),
                (
                    "moderator",
                    models.ForeignKey(
                        help_text="Moderator of the debate session",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="moderated_debates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Argument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("content", models.TextField(help_text="Content of the argument")),
                (
                    "vote_count",
                    models.IntegerField(
                        default=0, help_text="Net vote count for the argument"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="User who posted the argument",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="arguments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        help_text="Parent argument for threaded discussions",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="debate_arena.argument",
                    ),
                ),
                (
                    "debate_session",
                    models.ForeignKey(
                        help_text="Debate session this argument belongs to",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="arguments",
                        to="debate_arena.debatesession",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="VoteRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "vote_value",
                    models.IntegerField(help_text="Vote value, e.g., +1 or -1"),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Timestamp when the vote was cast"
                    ),
                ),
                (
                    "argument",
                    models.ForeignKey(
                        help_text="The argument being voted on",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vote_records",
                        to="debate_arena.argument",
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        help_text="User who cast the vote",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vote_records",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\ethikos\debate_arena\forms.py

```py

```


---
## apps\ethikos\home\apps.py

```py
from django.apps import AppConfig

class EthikosHomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ethikos.home'
    verbose_name = "Ethikos Home"

```


---
## apps\ethikos\home\admin.py

```py
# apps/ethikos/home/admin.py

from django.contrib import admin
from ethikos.home.models import DebateTopic, FeaturedDebate, PersonalizedRecommendation

@admin.register(DebateTopic)
class DebateTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'publish_date', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('title',)

@admin.register(FeaturedDebate)
class FeaturedDebateAdmin(admin.ModelAdmin):
    list_display = ('debate_topic', 'display_order', 'active', 'created_at')
    list_filter = ('active',)
    ordering = ('display_order',)

@admin.register(PersonalizedRecommendation)
class PersonalizedRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'debate_topic', 'score', 'created_at')
    list_filter = ('user',)
    search_fields = ('debate_topic__title',)
    ordering = ('-created_at',)

```


---
## apps\ethikos\home\models.py

```py
"""
File: apps/ethikos/ethikos_home/models.py

Purpose:
Create models for the debate landing portal, storing debate topics, featured items,
and personalized recommendations.
"""

from django.db import models
from common.base_models import BaseModel

class DebateTopic(BaseModel):
    """
    Represents a debate topic or category.
    """
    title = models.CharField(max_length=255, help_text="Title of the debate topic")
    description = models.TextField(help_text="Description of the debate topic")
    is_active = models.BooleanField(default=True, help_text="Whether the debate topic is active")
    publish_date = models.DateTimeField(null=True, blank=True, help_text="Publish date of the topic")

    def __str__(self):
        return self.title

class FeaturedDebate(BaseModel):
    """
    Marks a debate topic as featured on the landing portal.
    """
    debate_topic = models.ForeignKey(
        DebateTopic,
        on_delete=models.CASCADE,
        related_name="featured_entries",
        help_text="Featured debate topic"
    )
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display")
    active = models.BooleanField(default=True, help_text="Whether this featured entry is active")

    def __str__(self):
        return f"Featured: {self.debate_topic.title}"

class PersonalizedRecommendation(BaseModel):
    """
    Stores personalized debate topic recommendations for users.
    """
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="User receiving the recommendation"
    )
    debate_topic = models.ForeignKey(
        DebateTopic,
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="Recommended debate topic"
    )
    score = models.FloatField(default=0, help_text="Relevance score for the recommendation")

    def __str__(self):
        return f"Recommendation for {self.user}: {self.debate_topic.title}"

```


---
## apps\ethikos\home\serializers.py

```py
from rest_framework import serializers
from ethikos.home.models import DebateTopic, FeaturedDebate, PersonalizedRecommendation

class DebateTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateTopic
        fields = [
            'id',
            'title',
            'description',
            'is_active',
            'publish_date',
            'created_at',
            'updated_at'
        ]

class FeaturedDebateSerializer(serializers.ModelSerializer):
    debate_topic = DebateTopicSerializer(read_only=True)

    class Meta:
        model = FeaturedDebate
        fields = [
            'id',
            'debate_topic',
            'display_order',
            'active',
            'created_at',
            'updated_at'
        ]

class PersonalizedRecommendationSerializer(serializers.ModelSerializer):
    debate_topic = DebateTopicSerializer(read_only=True)

    class Meta:
        model = PersonalizedRecommendation
        fields = [
            'id',
            'user',
            'debate_topic',
            'score',
            'created_at',
            'updated_at'
        ]

```


---
## apps\ethikos\home\views.py

```py
# apps/ethikos/home/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ethikos.home.models import DebateTopic, FeaturedDebate, PersonalizedRecommendation
from ethikos.home.serializers import (
    DebateTopicSerializer,
    FeaturedDebateSerializer,
    PersonalizedRecommendationSerializer
)

logger = logging.getLogger(__name__)


class DebateTopicViewSet(viewsets.ModelViewSet):
    """
    Gère les sujets de débat.
    - List & Retrieve : tout utilisateur authentifié
    - Create/Update/Delete : uniquement les administrateurs
    """
    serializer_class = DebateTopicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']            # à ajuster selon votre modèle (ex. 'category', 'is_active', etc.)
    search_fields = ['title']                  # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'title']
    ordering = ['title']

    def get_queryset(self):
        qs = DebateTopic.objects.all()         # même logique que votre queryset initial
        logger.debug(
            "DebateTopic queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()            # conserve votre logique de création
        logger.info(
            "DebateTopic créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "DebateTopic mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "DebateTopic supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DebateTopicViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class FeaturedDebateViewSet(viewsets.ModelViewSet):
    """
    Gère les débats mis en avant.
    - List & Retrieve : tout utilisateur authentifié
    - Create/Update/Delete : uniquement les administrateurs
    """
    serializer_class = FeaturedDebateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']            # à ajuster selon votre modèle
    search_fields = ['topic__title']           # ou un autre champ pertinent
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = FeaturedDebate.objects.all()      # même logique que votre queryset initial
        logger.debug(
            "FeaturedDebate queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "FeaturedDebate créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "FeaturedDebate mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "FeaturedDebate supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans FeaturedDebateViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class PersonalizedRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lecture seule des recommandations personnalisées pour l'utilisateur connecté.
    """
    serializer_class = PersonalizedRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = PersonalizedRecommendation.objects.filter(user=self.request.user)
        logger.debug(
            "PersonalizedRecommendation queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans PersonalizedRecommendationViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\ethikos\home\urls.py

```py
# apps/ethikos/home/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.home.views import (
    DebateTopicViewSet,
    FeaturedDebateViewSet,
    PersonalizedRecommendationViewSet,
)

app_name = "home"

router = DefaultRouter()
router.register(r'debate_topics',                DebateTopicViewSet)
router.register(r'featured_debates',             FeaturedDebateViewSet)
router.register(r'personalized_recommendations', PersonalizedRecommendationViewSet)

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\ethikos\home\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DebateTopic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the debate topic", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(help_text="Description of the debate topic"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="Whether the debate topic is active"
                    ),
                ),
                (
                    "publish_date",
                    models.DateTimeField(
                        blank=True, help_text="Publish date of the topic", null=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FeaturedDebate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "display_order",
                    models.PositiveIntegerField(
                        default=0, help_text="Order for display"
                    ),
                ),
                (
                    "active",
                    models.BooleanField(
                        default=True, help_text="Whether this featured entry is active"
                    ),
                ),
                (
                    "debate_topic",
                    models.ForeignKey(
                        help_text="Featured debate topic",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="featured_entries",
                        to="home.debatetopic",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PersonalizedRecommendation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "score",
                    models.FloatField(
                        default=0, help_text="Relevance score for the recommendation"
                    ),
                ),
                (
                    "debate_topic",
                    models.ForeignKey(
                        help_text="Recommended debate topic",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommendations",
                        to="home.debatetopic",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User receiving the recommendation",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommendations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\ethikos\home\forms.py

```py

```


---
## apps\ethikos\knowledge_base\apps.py

```py
from django.apps import AppConfig

class EthikosKnowledgeBaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ethikos.knowledge_base'
    verbose_name = "Ethikos Knowledge Base"

```


---
## apps\ethikos\knowledge_base\admin.py

```py
# apps/ethikos/knowledge_base/admin.py

from django.contrib import admin
from ethikos.knowledge_base.models import DebateArchive

@admin.register(DebateArchive)
class DebateArchiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'debate_date', 'source', 'created_at')
    list_filter = ('debate_date',)
    search_fields = ('title', 'content')
    ordering = ('-debate_date',)

```


---
## apps\ethikos\knowledge_base\models.py

```py
"""
File: apps/ethikos/ethikos_knowledge_base/models.py

This module creates archival models for debates, philosophical texts,
and legal precedents. It supports full‑text search and filtering.
"""

from django.db import models
from common.base_models import BaseModel

class DebateArchive(BaseModel):
    """
    Archives debates and related texts for historical and research purposes.
    """
    title = models.CharField(max_length=255, help_text="Title of the archived debate or text")
    content = models.TextField(help_text="Full text content for search and analysis")
    debate_date = models.DateField(null=True, blank=True, help_text="Date of the debate or publication")
    source = models.CharField(max_length=255, null=True, blank=True, help_text="Source or reference of the material")
    tags = models.JSONField(null=True, blank=True, help_text="List of tags for filtering and search")

    def __str__(self):
        return self.title

```


---
## apps\ethikos\knowledge_base\serializers.py

```py
from rest_framework import serializers
from ethikos.knowledge_base.models import DebateArchive

class DebateArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateArchive
        fields = [
            'id',
            'title',
            'content',
            'debate_date',
            'source',
            'tags',
            'created_at',
            'updated_at'
        ]

```


---
## apps\ethikos\knowledge_base\views.py

```py
# apps/ethikos/knowledge_base/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ethikos.knowledge_base.models import DebateArchive
from ethikos.knowledge_base.serializers import DebateArchiveSerializer

logger = logging.getLogger(__name__)

class DebateArchiveViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer l'archivage des débats et des contenus de référence.
    """
    serializer_class = DebateArchiveSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['year']             # à ajuster selon vos champs métier
    search_fields = ['title', 'summary']    # à ajuster selon vos champs
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = DebateArchive.objects.all()   # même logique que votre queryset initial
        logger.debug(
            "DebateArchive queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()        # conserve votre logique de création
        logger.info(
            "DebateArchive créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DebateArchiveViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\ethikos\knowledge_base\urls.py

```py
# apps/ethikos/knowledge_base/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.knowledge_base.views import DebateArchiveViewSet

app_name = "knowledge_base"

router = DefaultRouter()
router.register(r"debate_archives", DebateArchiveViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\ethikos\knowledge_base\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DebateArchive",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the archived debate or text", max_length=255
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Full text content for search and analysis"
                    ),
                ),
                (
                    "debate_date",
                    models.DateField(
                        blank=True,
                        help_text="Date of the debate or publication",
                        null=True,
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        help_text="Source or reference of the material",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "tags",
                    models.JSONField(
                        blank=True,
                        help_text="List of tags for filtering and search",
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\ethikos\knowledge_base\forms.py

```py

```


---
## apps\ethikos\prioritization\apps.py

```py
from django.apps import AppConfig

class EthikosPrioritizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ethikos.prioritization'
    verbose_name = "Ethikos Prioritization"

```


---
## apps\ethikos\prioritization\admin.py

```py
# apps/ethikos/prioritization/admin.py

from django.contrib import admin
from ethikos.prioritization.models import DebatePrioritization

@admin.register(DebatePrioritization)
class DebatePrioritizationAdmin(admin.ModelAdmin):
    list_display = ('debate_session', 'ranking_score', 'created_at')
    list_filter = ('debate_session',)
    ordering = ('-created_at',)

```


---
## apps\ethikos\prioritization\models.py

```py
"""
File: apps/ethikos/ethikos_prioritization/models.py

This module develops models to rank and filter debates based on engagement,
credibility, and reputation integration.
"""

from django.db import models
from common.base_models import BaseModel

class DebatePrioritization(BaseModel):
    """
    Ranks a debate session based on computed criteria.
    """
    debate_session = models.ForeignKey(
        "debate_arena.DebateSession",
        on_delete=models.CASCADE,
        related_name="prioritizations",
        help_text="Debate session being ranked"
    )
    ranking_score = models.FloatField(help_text="Computed ranking score for the debate")
    criteria = models.JSONField(null=True, blank=True, help_text="JSON data detailing the ranking criteria")
    notes = models.TextField(null=True, blank=True, help_text="Additional notes or rationale for the ranking")

    def __str__(self):
        return f"Prioritization for {self.debate_session.topic}: Score {self.ranking_score}"

```


---
## apps\ethikos\prioritization\serializers.py

```py
from rest_framework import serializers
from ethikos.prioritization.models import DebatePrioritization

class DebatePrioritizationSerializer(serializers.ModelSerializer):
    debate_session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DebatePrioritization
        fields = [
            'id',
            'debate_session',
            'ranking_score',
            'criteria',
            'notes',
            'created_at',
            'updated_at'
        ]

```


---
## apps\ethikos\prioritization\views.py

```py
# apps/ethikos/prioritization/views.py
from rest_framework import viewsets, permissions
from ethikos.prioritization.models import DebatePrioritization
from ethikos.prioritization.serializers import DebatePrioritizationSerializer

class DebatePrioritizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer le classement et le filtrage des débats.
    Les critères d'engagement et de crédibilité sont pris en compte dans le score.
    """
    serializer_class = DebatePrioritizationSerializer

    def get_queryset(self):
        # Toutes les priorisations sont visibles
        return DebatePrioritization.objects.all()

    def get_permissions(self):
        # Lecture pour tout utilisateur authentifié, écriture réservée aux admins
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

```


---
## apps\ethikos\prioritization\urls.py

```py
# apps/ethikos/prioritization/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.prioritization.views import DebatePrioritizationViewSet

app_name = "prioritization"

router = DefaultRouter()
router.register(r"debate_prioritizations", DebatePrioritizationViewSet, basename="debateprioritization")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\ethikos\prioritization\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("debate_arena", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DebatePrioritization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "ranking_score",
                    models.FloatField(
                        help_text="Computed ranking score for the debate"
                    ),
                ),
                (
                    "criteria",
                    models.JSONField(
                        blank=True,
                        help_text="JSON data detailing the ranking criteria",
                        null=True,
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Additional notes or rationale for the ranking",
                        null=True,
                    ),
                ),
                (
                    "debate_session",
                    models.ForeignKey(
                        help_text="Debate session being ranked",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prioritizations",
                        to="debate_arena.debatesession",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\ethikos\prioritization\forms.py

```py

```


---
## apps\ethikos\resolution\apps.py

```py
from django.apps import AppConfig

class EthikosResolutionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ethikos.resolution'
    verbose_name = "Ethikos Resolution"

```


---
## apps\ethikos\resolution\admin.py

```py
# apps/ethikos/resolution/admin.py

from django.contrib import admin
from ethikos.resolution.models import DebateResolution

@admin.register(DebateResolution)
class DebateResolutionAdmin(admin.ModelAdmin):
    list_display = ('debate_session', 'approved_by', 'approved_at', 'created_at')
    search_fields = ('debate_session__topic',)
    ordering = ('-approved_at',)

```


---
## apps\ethikos\resolution\models.py

```py
"""
File: apps/ethikos/ethikos_resolution/models.py

This module defines models for documenting final debate resolutions.
It includes detailed decision histories and audit trails.
"""

from django.db import models
from common.base_models import BaseModel

class DebateResolution(BaseModel):
    """
    Documents the final resolution of a debate session.
    """
    debate_session = models.OneToOneField(
        "debate_arena.DebateSession",
        on_delete=models.CASCADE,
        related_name="resolution",
        help_text="Debate session for which this resolution applies"
    )
    resolution_text = models.TextField(help_text="Final resolution details and decisions")
    decision_history = models.JSONField(
        null=True,
        blank=True,
        help_text="JSON record of decision history and audit trail"
    )
    approved_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_resolutions",
        help_text="User who approved the resolution"
    )
    approved_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the resolution was approved")

    def __str__(self):
        return f"Resolution for {self.debate_session.topic}"

```


---
## apps\ethikos\resolution\serializers.py

```py
from rest_framework import serializers
from ethikos.resolution.models import DebateResolution

class DebateResolutionSerializer(serializers.ModelSerializer):
    debate_session = serializers.PrimaryKeyRelatedField(read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DebateResolution
        fields = [
            'id',
            'debate_session',
            'resolution_text',
            'decision_history',
            'approved_by',
            'approved_at',
            'created_at',
            'updated_at'
        ]

```


---
## apps\ethikos\resolution\views.py

```py
# apps/ethikos/resolution/views.py

from rest_framework import viewsets, permissions
from ethikos.resolution.models import DebateResolution
from ethikos.resolution.serializers import DebateResolutionSerializer

class DebateResolutionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les résolutions de débats.
    Chaque résolution inclut l'audit trail complet des décisions.
    """
    serializer_class = DebateResolutionSerializer

    def get_queryset(self):
        # Toutes les résolutions sont visibles, la logique métier peut filtrer si nécessaire
        return DebateResolution.objects.all()

    def get_permissions(self):
        # Lecture pour tout utilisateur authentifié, écriture réservée aux administrateurs
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

```


---
## apps\ethikos\resolution\urls.py

```py
# apps/ethikos/resolution/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.resolution.views import DebateResolutionViewSet

app_name = "resolution"

router = DefaultRouter()
router.register(
    r"debate_resolutions",
    DebateResolutionViewSet,
    basename="debateresolution"
)

urlpatterns = [
    path(
        "",
        include((router.urls, app_name), namespace=app_name)
    ),
]

```


---
## apps\ethikos\resolution\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("debate_arena", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DebateResolution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "resolution_text",
                    models.TextField(
                        help_text="Final resolution details and decisions"
                    ),
                ),
                (
                    "decision_history",
                    models.JSONField(
                        blank=True,
                        help_text="JSON record of decision history and audit trail",
                        null=True,
                    ),
                ),
                (
                    "approved_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="Timestamp when the resolution was approved",
                        null=True,
                    ),
                ),
                (
                    "approved_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="User who approved the resolution",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approved_resolutions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "debate_session",
                    models.OneToOneField(
                        help_text="Debate session for which this resolution applies",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resolution",
                        to="debate_arena.debatesession",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\ethikos\resolution\forms.py

```py

```


---
## apps\ethikos\stats\apps.py

```py
from django.apps import AppConfig

class EthikosStatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ethikos.stats'
    verbose_name = "Ethikos Stats"

```


---
## apps\ethikos\stats\admin.py

```py
# apps/ethikos/stats/admin.py

from django.contrib import admin
from ethikos.stats.models import DebateStatistic, DebateEventLog

@admin.register(DebateStatistic)
class DebateStatisticAdmin(admin.ModelAdmin):
    list_display = ('debate_session', 'metric_name', 'value', 'recorded_at')
    list_filter = ('debate_session', 'metric_name')
    ordering = ('-recorded_at',)

@admin.register(DebateEventLog)
class DebateEventLogAdmin(admin.ModelAdmin):
    list_display = ('debate_session', 'event_type', 'timestamp')
    list_filter = ('debate_session', 'event_type')
    ordering = ('-timestamp',)

```


---
## apps\ethikos\stats\models.py

```py
"""
File: apps/ethikos/ethikos_stats/models.py

This module builds models to capture statistical data for debates.
It supports time‑series analytics and logs events for dashboard displays.
"""

from django.db import models
from common.base_models import BaseModel

class DebateStatistic(BaseModel):
    """
    Represents a time-series statistical record for a debate session.
    """
    debate_session = models.ForeignKey(
        "debate_arena.DebateSession",
        on_delete=models.CASCADE,
        related_name="statistics",
        help_text="Associated debate session"
    )
    metric_name = models.CharField(max_length=100, help_text="Name of the metric (e.g., total_votes, active_participants)")
    value = models.FloatField(help_text="Recorded value of the metric")
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the metric was recorded")

    def __str__(self):
        return f"{self.metric_name} for {self.debate_session.topic}: {self.value}"

class DebateEventLog(BaseModel):
    """
    Logs events related to debates for analytics and audit purposes.
    """
    debate_session = models.ForeignKey(
        "debate_arena.DebateSession",
        on_delete=models.CASCADE,
        related_name="event_logs",
        help_text="Debate session associated with this event"
    )
    event_type = models.CharField(max_length=100, help_text="Type of event (e.g., 'argument_posted', 'vote_cast')")
    description = models.TextField(null=True, blank=True, help_text="Detailed description of the event")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the event")

    def __str__(self):
        return f"Event {self.event_type} at {self.timestamp}"

```


---
## apps\ethikos\stats\serializers.py

```py
from rest_framework import serializers
from ethikos.stats.models import DebateStatistic, DebateEventLog

class DebateStatisticSerializer(serializers.ModelSerializer):
    debate_session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DebateStatistic
        fields = [
            'id',
            'debate_session',
            'metric_name',
            'value',
            'recorded_at',
            'created_at',
            'updated_at'
        ]

class DebateEventLogSerializer(serializers.ModelSerializer):
    debate_session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DebateEventLog
        fields = [
            'id',
            'debate_session',
            'event_type',
            'description',
            'timestamp',
            'created_at',
            'updated_at'
        ]

```


---
## apps\ethikos\stats\views.py

```py
from rest_framework import viewsets, permissions
from ethikos.stats.models import DebateStatistic, DebateEventLog
from ethikos.stats.serializers import (
    DebateStatisticSerializer,
    DebateEventLogSerializer
)

class DebateStatisticViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les statistiques des débats (ex. : nombre de votes, participants actifs).
    """
    serializer_class = DebateStatisticSerializer

    def get_queryset(self):
        # Liste globale : on ne filtre pas par utilisateur
        return DebateStatistic.objects.all()

    def get_permissions(self):
        # Lecture pour tout utilisateur authentifié, écriture réservée aux admins
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class DebateEventLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour consulter et enregistrer les logs d'événements des débats.
    """
    serializer_class = DebateEventLogSerializer

    def get_queryset(self):
        # Logs globaux : on ne filtre pas par utilisateur
        return DebateEventLog.objects.all()

    def get_permissions(self):
        # Lecture pour tout utilisateur authentifié, écriture réservée aux admins
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

```


---
## apps\ethikos\stats\urls.py

```py
# apps/ethikos/stats/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.stats.views import DebateStatisticViewSet, DebateEventLogViewSet

app_name = "stats"

router = DefaultRouter()
router.register(r"debate_statistics", DebateStatisticViewSet)
router.register(r"debate_event_logs", DebateEventLogViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\ethikos\stats\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("debate_arena", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DebateEventLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "event_type",
                    models.CharField(
                        help_text="Type of event (e.g., 'argument_posted', 'vote_cast')",
                        max_length=100,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Detailed description of the event",
                        null=True,
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Timestamp of the event"
                    ),
                ),
                (
                    "debate_session",
                    models.ForeignKey(
                        help_text="Debate session associated with this event",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_logs",
                        to="debate_arena.debatesession",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DebateStatistic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "metric_name",
                    models.CharField(
                        help_text="Name of the metric (e.g., total_votes, active_participants)",
                        max_length=100,
                    ),
                ),
                ("value", models.FloatField(help_text="Recorded value of the metric")),
                (
                    "recorded_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Timestamp when the metric was recorded",
                    ),
                ),
                (
                    "debate_session",
                    models.ForeignKey(
                        help_text="Associated debate session",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="statistics",
                        to="debate_arena.debatesession",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\ethikos\stats\forms.py

```py

```


---
## apps\keenkonnect\collab_spaces\apps.py

```py
from django.apps import AppConfig

class KeenkonnectCollabSpacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keenkonnect.collab_spaces'
    verbose_name = "Keenkonnect Collab Spaces"

```


---
## apps\keenkonnect\collab_spaces\admin.py

```py
# apps/keenkonnect/collab_spaces/admin.py

from django.contrib import admin
from keenkonnect.collab_spaces.models import CollabSpace, Document, ChatMessage

@admin.register(CollabSpace)
class CollabSpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'participant_count', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = "Nombre de participants"

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'collab_space', 'uploaded_by', 'uploaded_at')
    list_filter = ('collab_space', 'uploaded_by')
    search_fields = ('title',)
    ordering = ('-uploaded_at',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('collab_space', 'sender', 'is_read', 'created_at')
    list_filter = ('is_read', 'sender')
    search_fields = ('message',)
    ordering = ('-created_at',)
    
    actions = ['mark_messages_as_read']

    def mark_messages_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} message(s) marqué(s) comme lu(s).")
    mark_messages_as_read.short_description = "Marquer les messages sélectionnés comme lus"

```


---
## apps\keenkonnect\collab_spaces\models.py

```py
"""
File: \apps\keenkonnect\collab_spaces/models.py

This module defines models for real-time collaboration spaces.
It includes models for collaborative workspaces, document sharing, and chat messages.
"""

from django.db import models
from common.base_models import BaseModel

class CollabSpace(BaseModel):
    """
    Represents a collaborative workspace.
    """
    name = models.CharField(max_length=255, help_text="Name of the collaboration space.")
    description = models.TextField(null=True, blank=True, help_text="Description of the space.")
    created_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="collab_spaces_created",
        help_text="User who created the space."
    )
    participants = models.ManyToManyField(
        "core.CustomUser",
        related_name="collab_spaces",
        help_text="Users participating in the space."
    )
    is_active = models.BooleanField(default=True, help_text="Indicates if the space is active.")

    def __str__(self):
        return self.name

class Document(BaseModel):
    """
    Represents a document shared within a collaboration space.
    """
    collab_space = models.ForeignKey(
        CollabSpace,
        on_delete=models.CASCADE,
        related_name="documents",
        help_text="Collaboration space where the document is shared."
    )
    title = models.CharField(max_length=255, help_text="Title of the document.")
    file = models.FileField(upload_to="collab_documents/", help_text="Uploaded file for the document.")
    description = models.TextField(null=True, blank=True, help_text="Optional description.")
    uploaded_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_documents",
        help_text="User who uploaded the document."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Upload timestamp.")

    def __str__(self):
        return self.title

class ChatMessage(BaseModel):
    """
    Represents a chat message within a collaboration space.
    """
    collab_space = models.ForeignKey(
        CollabSpace,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        help_text="Collaboration space where the message was sent."
    )
    sender = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="chat_messages",
        help_text="User who sent the message."
    )
    message = models.TextField(help_text="Content of the chat message.")
    is_read = models.BooleanField(default=False, help_text="Indicates if the message has been read.")

    def __str__(self):
        return f"Message from {self.sender} in {self.collab_space.name}"

```


---
## apps\keenkonnect\collab_spaces\serializers.py

```py
from rest_framework import serializers
from keenkonnect.collab_spaces.models import CollabSpace, Document, ChatMessage

class CollabSpaceSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CollabSpace
        fields = [
            'id',
            'name',
            'description',
            'created_by',
            'participants',
            'is_active',
            'created_at',
            'updated_at'
        ]

class DocumentSerializer(serializers.ModelSerializer):
    collab_space = serializers.PrimaryKeyRelatedField(read_only=True)
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'collab_space',
            'title',
            'file',
            'description',
            'uploaded_by',
            'uploaded_at',
            'created_at',
            'updated_at'
        ]

class ChatMessageSerializer(serializers.ModelSerializer):
    collab_space = serializers.PrimaryKeyRelatedField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'collab_space',
            'sender',
            'message',
            'created_at',
            'updated_at'
        ]

```


---
## apps\keenkonnect\collab_spaces\views.py

```py
# apps/keenkonnect/collab_spaces/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from keenkonnect.collab_spaces.models import CollabSpace, Document, ChatMessage
from keenkonnect.collab_spaces.serializers import (
    CollabSpaceSerializer,
    DocumentSerializer,
    ChatMessageSerializer
)
# Si vous utilisez une tâche Celery pour notifier en temps réel, décommentez :
# from keenkonnect.collab_spaces.tasks import notify_new_chat_message

logger = logging.getLogger(__name__)


class CollabSpaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les espaces de collaboration.
    """
    serializer_class = CollabSpaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['participants']              # À ajuster selon votre modèle
    search_fields = ['name', 'description']          # À adapter aux champs réels
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = CollabSpace.objects.filter(participants=self.request.user)
        logger.debug(
            "CollabSpace queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        collab_space = serializer.save()
        collab_space.participants.add(self.request.user)
        logger.info(
            "CollabSpace créé (id=%s) par %s",
            collab_space.pk, self.request.user
        )
        return collab_space

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_participant(self, request, pk=None):
        """
        Ajoute un participant (user_id dans request.data) à l’espace.
        """
        collab_space = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            logger.warning("add_participant sans user_id par %s", request.user)
            return Response(
                {"error": "Le champ 'user_id' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            collab_space.participants.add(user_id)
            logger.info(
                "Utilisateur %s ajouté à CollabSpace id=%s par %s",
                user_id, collab_space.pk, request.user
            )
            return Response(self.get_serializer(collab_space).data, status=status.HTTP_200_OK)
        except Exception as exc:
            logger.exception(
                "Erreur add_participant pour CollabSpace id=%s par %s: %s",
                collab_space.pk, request.user, exc
            )
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CollabSpaceViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les documents partagés dans un espace de collaboration.
    """
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['collab_space']               # À ajuster selon votre modèle
    search_fields = ['title', 'filename']             # À adapter aux champs réels
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Document.objects.filter(collab_space__participants=self.request.user)
        logger.debug(
            "Document queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        doc = serializer.save()
        logger.info(
            "Document créé (id=%s) par %s",
            doc.pk, self.request.user
        )
        return doc

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DocumentViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les messages de chat dans un espace de collaboration.
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['collab_space', 'sender']     # À ajuster selon votre modèle
    search_fields = ['message']                       # À adapter au champ réel
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        qs = ChatMessage.objects.filter(collab_space__participants=self.request.user)
        logger.debug(
            "ChatMessage queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        logger.info(
            "ChatMessage créé (id=%s) par %s",
            message.pk, self.request.user
        )
        # Si notification en temps réel :
        # notify_new_chat_message.delay(message.id)
        return message

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        """
        Marque un message comme lu.
        """
        message = self.get_object()
        try:
            message.is_read = True
            message.save()
            logger.info(
                "ChatMessage id=%s marqué comme lu par %s",
                message.pk, request.user
            )
            return Response(self.get_serializer(message).data, status=status.HTTP_200_OK)
        except Exception as exc:
            logger.exception(
                "Erreur dans mark_as_read pour ChatMessage id=%s par %s: %s",
                message.pk, request.user, exc
            )
            return Response(
                {"detail": "Impossible de marquer le message comme lu."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ChatMessageViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\keenkonnect\collab_spaces\urls.py

```py
# apps/keenkonnect/collab_spaces/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.collab_spaces.views import CollabSpaceViewSet, DocumentViewSet, ChatMessageViewSet

app_name = 'collab_spaces'

router = DefaultRouter()
router.register(r'collab_spaces', CollabSpaceViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'chat_messages', ChatMessageViewSet)

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\keenkonnect\collab_spaces\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("message", models.TextField(help_text="Content of the chat message.")),
                (
                    "is_read",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if the message has been read.",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CollabSpace",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the collaboration space.", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Description of the space.", null=True
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="Indicates if the space is active."
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the document.", max_length=255
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        help_text="Uploaded file for the document.",
                        upload_to="collab_documents/",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Optional description.", null=True
                    ),
                ),
                (
                    "uploaded_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Upload timestamp."
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\keenkonnect\collab_spaces\forms.py

```py

```


---
## apps\keenkonnect\expert_match\apps.py

```py
from django.apps import AppConfig

class KeenkonnectExpertMatchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keenkonnect.expert_match'
    verbose_name = "Keenkonnect Expert Match"

```


---
## apps\keenkonnect\expert_match\admin.py

```py
# apps/keenkonnect/expert_match/admin.py

from django.contrib import admin
from keenkonnect.expert_match.models import ExpertMatchRequest, CandidateProfile, MatchScore

@admin.register(ExpertMatchRequest)
class ExpertMatchRequestAdmin(admin.ModelAdmin):
    list_display = ('project', 'requested_by', 'created_at')
    search_fields = ('project__title', 'requested_by__username')
    ordering = ('-created_at',)
    
    actions = ['trigger_matching']

    def trigger_matching(self, request, queryset):
        # Ici, vous pouvez intégrer un appel à une tâche asynchrone de matching
        count = queryset.count()
        self.message_user(request, f"Processus de matching déclenché pour {count} demande(s).")
    trigger_matching.short_description = "Déclencher le processus de matching pour les demandes sélectionnées"

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation_score', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)

@admin.register(MatchScore)
class MatchScoreAdmin(admin.ModelAdmin):
    list_display = ('match_request', 'candidate', 'score', 'created_at')
    search_fields = ('match_request__project__title', 'candidate__user__username')
    ordering = ('-created_at',)

```


---
## apps\keenkonnect\expert_match\models.py

```py
"""
File: apps/keenkonnectexpert_match/models.py

This module defines models for matching projects with experts.
It includes models for match requests, candidate profiles, and compatibility scoring.
"""

from django.db import models
from common.base_models import BaseModel

class ExpertMatchRequest(BaseModel):
    """
    Represents a request for expert matching for a project.
    """
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="expert_match_requests",
        help_text="Project needing expert matching."
    )
    requested_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="expert_match_requests",
        help_text="User who initiated the match request."
    )
    description = models.TextField(help_text="Description of the expertise required.")
    criteria = models.JSONField(null=True, blank=True, help_text="JSON detailing matching criteria.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the request was created.")

    def __str__(self):
        return f"Expert Match Request for {self.project.title}"

class CandidateProfile(BaseModel):
    """
    Represents a candidate's profile for expert matching.
    """
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="candidate_profiles",
        help_text="User associated with this candidate profile."
    )
    skills = models.JSONField(null=True, blank=True, help_text="JSON data representing skills and expertise.")
    reputation_score = models.FloatField(default=0, help_text="Reputation score from the ekoh system.")

    def __str__(self):
        return f"Candidate Profile for {self.user}"

class MatchScore(BaseModel):
    """
    Represents the compatibility score between a match request and a candidate.
    """
    match_request = models.ForeignKey(
        ExpertMatchRequest,
        on_delete=models.CASCADE,
        related_name="match_scores",
        help_text="The expert match request."
    )
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="match_scores",
        help_text="Candidate profile being evaluated."
    )
    score = models.FloatField(help_text="Computed compatibility score.")

    def __str__(self):
        return f"Match Score: {self.candidate.user} - {self.score}"

```


---
## apps\keenkonnect\expert_match\serializers.py

```py
from rest_framework import serializers
from keenkonnect.expert_match.models import ExpertMatchRequest, CandidateProfile, MatchScore

class ExpertMatchRequestSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    requested_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ExpertMatchRequest
        fields = [
            'id',
            'project',
            'requested_by',
            'description',
            'criteria',
            'created_at',
            'updated_at'
        ]

class CandidateProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CandidateProfile
        fields = [
            'id',
            'user',
            'skills',
            'reputation_score',
            'created_at',
            'updated_at'
        ]

class MatchScoreSerializer(serializers.ModelSerializer):
    match_request = serializers.PrimaryKeyRelatedField(read_only=True)
    candidate = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MatchScore
        fields = [
            'id',
            'match_request',
            'candidate',
            'score',
            'created_at',
            'updated_at'
        ]

```


---
## apps\keenkonnect\expert_match\views.py

```py
# apps/keenkonnect/expert_match/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from keenkonnect.expert_match.models import ExpertMatchRequest, CandidateProfile, MatchScore
from keenkonnect.expert_match.serializers import (
    ExpertMatchRequestSerializer,
    CandidateProfileSerializer,
    MatchScoreSerializer
)

logger = logging.getLogger(__name__)


class ExpertMatchRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les demandes de mise en relation avec des experts.
    """
    serializer_class = ExpertMatchRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']               # à ajuster selon votre modèle (ex. 'status', 'requester__username')
    search_fields = ['topic', 'description']    # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = ExpertMatchRequest.objects.all()   # même logique que votre queryset initial
        logger.debug(
            "ExpertMatchRequest queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()            # conserve votre logique de création
        logger.info(
            "ExpertMatchRequest créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ExpertMatchRequestViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def trigger_match(self, request, pk=None):
        """
        Action personnalisée pour déclencher le processus de matching.
        (Ici, vous pouvez appeler une tâche asynchrone par exemple.)
        """
        match_request = self.get_object()
        try:
            # Exemple : déclencher la tâche asynchrone
            # trigger_expert_matching.delay(match_request.id)
            logger.info(
                "Matching déclenché pour ExpertMatchRequest id=%s par %s",
                match_request.id, request.user
            )
            return Response(
                {"status": "Matching déclenché", "match_request_id": match_request.id},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception(
                "Erreur lors du déclenchement du matching de %s par %s : %s",
                match_request.id, request.user, e
            )
            return Response(
                {"detail": "Impossible de déclencher le matching."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CandidateProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les profils candidats pour le matching.
    """
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['expertise', 'location']  # à ajuster selon votre modèle
    search_fields = ['name', 'bio']               # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = CandidateProfile.objects.all()       # même logique que votre queryset initial
        logger.debug(
            "CandidateProfile queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()              # conserve votre logique de création
        logger.info(
            "CandidateProfile créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CandidateProfileViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class MatchScoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour consulter et enregistrer les scores de compatibilité.
    """
    serializer_class = MatchScoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['match_request', 'candidate']  # à ajuster selon votre modèle
    ordering_fields = ['score', 'created_at']
    ordering = ['-score']

    def get_queryset(self):
        qs = MatchScore.objects.all()             # même logique que votre queryset initial
        logger.debug(
            "MatchScore queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()              # conserve votre logique de création
        logger.info(
            "MatchScore créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans MatchScoreViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\keenkonnect\expert_match\urls.py

```py
# apps/keenkonnect/expert_match/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.expert_match.views import (
    ExpertMatchRequestViewSet,
    CandidateProfileViewSet,
    MatchScoreViewSet,
)

app_name = "expert_match"

router = DefaultRouter()
router.register(r"expert_match_requests", ExpertMatchRequestViewSet)
router.register(r"candidate_profiles",    CandidateProfileViewSet)
router.register(r"match_scores",          MatchScoreViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\keenkonnect\expert_match\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CandidateProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "skills",
                    models.JSONField(
                        blank=True,
                        help_text="JSON data representing skills and expertise.",
                        null=True,
                    ),
                ),
                (
                    "reputation_score",
                    models.FloatField(
                        default=0, help_text="Reputation score from the ekoh system."
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User associated with this candidate profile.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidate_profiles",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExpertMatchRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "description",
                    models.TextField(
                        help_text="Description of the expertise required."
                    ),
                ),
                (
                    "criteria",
                    models.JSONField(
                        blank=True,
                        help_text="JSON detailing matching criteria.",
                        null=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Timestamp when the request was created.",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="Project needing expert matching.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expert_match_requests",
                        to="projects.project",
                    ),
                ),
                (
                    "requested_by",
                    models.ForeignKey(
                        help_text="User who initiated the match request.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="expert_match_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MatchScore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("score", models.FloatField(help_text="Computed compatibility score.")),
                (
                    "candidate",
                    models.ForeignKey(
                        help_text="Candidate profile being evaluated.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_scores",
                        to="expert_match.candidateprofile",
                    ),
                ),
                (
                    "match_request",
                    models.ForeignKey(
                        help_text="The expert match request.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="match_scores",
                        to="expert_match.expertmatchrequest",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\keenkonnect\expert_match\forms.py

```py

```


---
## apps\keenkonnect\gap_analysis\apps.py

```py

```


---
## apps\keenkonnect\gap_analysis\admin.py

```py
# apps/keenkonnect/gap_analysis/admin.py

from django.contrib import admin
from keenkonnect.gap_analysis.models import GapAnalysis

@admin.register(GapAnalysis)
class GapAnalysisAdmin(admin.ModelAdmin):
    list_display = ('project', 'planned_progress', 'actual_progress', 'gap', 'created_at')
    list_filter = ('project__status',)  # Si le projet possède un champ "status"
    search_fields = ('project__title',)
    ordering = ('-created_at',)

```


---
## apps\keenkonnect\gap_analysis\models.py

```py
"""
File: apps/keenkonnectgap_analysis/models.py

This module defines models to record gap analysis data for projects.
It compares planned versus actual progress and stores recommendations.
"""

from django.db import models
from common.base_models import BaseModel

class GapAnalysis(BaseModel):
    """
    Represents a gap analysis record for a project.
    """
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="gap_analyses",
        help_text="Project for which the gap analysis is performed."
    )
    planned_progress = models.PositiveIntegerField(help_text="Planned progress percentage.")
    actual_progress = models.PositiveIntegerField(help_text="Actual progress percentage.")
    gap = models.PositiveIntegerField(help_text="Difference between planned and actual progress.")
    recommendations = models.TextField(null=True, blank=True, help_text="Recommendations to close the gap.")

    def __str__(self):
        return f"Gap Analysis for {self.project.title}"

```


---
## apps\keenkonnect\gap_analysis\serializers.py

```py
from rest_framework import serializers
from keenkonnect.gap_analysis.models import GapAnalysis

class GapAnalysisSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GapAnalysis
        fields = [
            'id',
            'project',
            'planned_progress',
            'actual_progress',
            'gap',
            'recommendations',
            'created_at',
            'updated_at'
        ]

```


---
## apps\keenkonnect\gap_analysis\views.py

```py
# apps/keenkonnect/gap_analysis/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from keenkonnect.gap_analysis.models import GapAnalysis
from keenkonnect.gap_analysis.serializers import GapAnalysisSerializer

logger = logging.getLogger(__name__)

class GapAnalysisViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les enregistrements d'analyse d'écart pour les projets.
    Permet de comparer le progrès prévu et réel et de stocker des recommandations.
    """
    serializer_class = GapAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'project',      # à ajuster selon votre champ de relation vers le projet
        'status',       # ex. 'open', 'closed', etc.
    ]
    search_fields = [
        'title',        # à adapter si votre modèle utilise ce champ
        'recommendations',
    ]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = GapAnalysis.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "GapAnalysis queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()   # conserve votre logique de création
        logger.info(
            "GapAnalysis créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans GapAnalysisViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\keenkonnect\gap_analysis\urls.py

```py
# apps/keenkonnect/gap_analysis/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.gap_analysis.views import GapAnalysisViewSet

app_name = "gap_analysis"

router = DefaultRouter()
router.register(r"gap_analyses", GapAnalysisViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\keenkonnect\gap_analysis\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GapAnalysis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "planned_progress",
                    models.PositiveIntegerField(
                        help_text="Planned progress percentage."
                    ),
                ),
                (
                    "actual_progress",
                    models.PositiveIntegerField(
                        help_text="Actual progress percentage."
                    ),
                ),
                (
                    "gap",
                    models.PositiveIntegerField(
                        help_text="Difference between planned and actual progress."
                    ),
                ),
                (
                    "recommendations",
                    models.TextField(
                        blank=True,
                        help_text="Recommendations to close the gap.",
                        null=True,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="Project for which the gap analysis is performed.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gap_analyses",
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\keenkonnect\gap_analysis\forms.py

```py

```


---
## apps\keenkonnect\knowledge_hub\apps.py

```py
from django.apps import AppConfig

class KeenkonnectKnowledgeHubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keenkonnect.knowledge_hub'
    verbose_name = "Keenkonnect Knowledge Hub"

```


---
## apps\keenkonnect\knowledge_hub\admin.py

```py
# apps/keenkonnect/knowledge_hub/admin.py

from django.contrib import admin
from keenkonnect.knowledge_hub.models import KnowledgeDocument, DocumentRevision

class DocumentRevisionInline(admin.TabularInline):
    model = DocumentRevision
    extra = 0
    fields = ('revision_number', 'changes', 'revised_by', 'revised_at')
    readonly_fields = ('revised_at',)

@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('title',)
    inlines = [DocumentRevisionInline]

@admin.register(DocumentRevision)
class DocumentRevisionAdmin(admin.ModelAdmin):
    list_display = ('knowledge_document', 'revision_number', 'revised_by', 'revised_at')
    list_filter = ('knowledge_document',)
    search_fields = ('knowledge_document__title',)
    ordering = ('-revised_at',)

```


---
## apps\keenkonnect\knowledge_hub\models.py

```py
"""
File: apps/keenkonnect/keenKnowledgeHub/models.py

This module defines models for a repository of blueprints, research documents,
and version-controlled designs.
"""

from django.db import models
from common.base_models import BaseModel

class KnowledgeDocument(BaseModel):
    """
    Represents a document such as a blueprint or research paper.
    """
    title = models.CharField(max_length=255, help_text="Title of the document.")
    description = models.TextField(null=True, blank=True, help_text="Description of the document.")
    document_file = models.FileField(upload_to="knowledge_documents/", help_text="Uploaded document file.")
    version = models.CharField(max_length=50, default="1.0", help_text="Document version.")
    created_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="knowledge_documents",
        help_text="User who created/uploaded the document."
    )

    def __str__(self):
        return f"{self.title} (v{self.version})"

class DocumentRevision(BaseModel):
    """
    Represents a revision of a knowledge document.
    """
    knowledge_document = models.ForeignKey(
        KnowledgeDocument,
        on_delete=models.CASCADE,
        related_name="revisions",
        help_text="The document to which this revision belongs."
    )
    revision_number = models.CharField(max_length=50, help_text="Revision number or identifier.")
    changes = models.TextField(help_text="Description of the changes in this revision.")
    revised_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="document_revisions",
        help_text="User who made the revision."
    )
    revised_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the revision was made.")

    def __str__(self):
        return f"{self.knowledge_document.title} Revision {self.revision_number}"

```


---
## apps\keenkonnect\knowledge_hub\serializers.py

```py
from rest_framework import serializers
from keenkonnect.knowledge_hub.models import KnowledgeDocument, DocumentRevision

class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeDocument
        fields = [
            'id',
            'title',
            'description',
            'document_file',
            'version',
            'created_by',
            'created_at',
            'updated_at'
        ]

class DocumentRevisionSerializer(serializers.ModelSerializer):
    knowledge_document = serializers.PrimaryKeyRelatedField(read_only=True)
    revised_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DocumentRevision
        fields = [
            'id',
            'knowledge_document',
            'revision_number',
            'changes',
            'revised_by',
            'revised_at',
            'created_at',
            'updated_at'
        ]

```


---
## apps\keenkonnect\knowledge_hub\views.py

```py
# apps/keenkonnect/knowledge_hub/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from keenkonnect.knowledge_hub.models import KnowledgeDocument, DocumentRevision
from keenkonnect.knowledge_hub.serializers import (
    KnowledgeDocumentSerializer,
    DocumentRevisionSerializer
)
# Exemple : Importer une tâche asynchrone pour gérer la révision de document
# from keenkonnect.knowledge_hub.tasks import trigger_document_revision

logger = logging.getLogger(__name__)

class KnowledgeDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les documents du Knowledge Hub.
    """
    serializer_class = KnowledgeDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']            # à ajuster si vous avez un champ 'status'
    search_fields = ['title', 'content']     # à ajuster selon vos champs
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = KnowledgeDocument.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "KnowledgeDocument queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()           # conserve votre logique de création
        logger.info(
            "KnowledgeDocument créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans KnowledgeDocumentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def revise(self, request, pk=None):
        """
        Action personnalisée pour lancer une révision du document.
        """
        document = self.get_object()
        try:
            # Exemple : déclencher une tâche asynchrone de révision
            # trigger_document_revision.delay(document.id)
            logger.info(
                "Révision déclenchée pour KnowledgeDocument id=%s par %s",
                document.id, request.user
            )
            return Response(
                {"status": "Révision déclenchée", "document_id": document.id},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception(
                "Erreur lors de la révision de %s par %s : %s",
                document.id, request.user, e
            )
            return Response(
                {"detail": "Impossible de lancer la révision."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DocumentRevisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les révisions des documents.
    """
    serializer_class = DocumentRevisionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document']         # à ajuster si besoin
    ordering = ['created_at']

    def get_queryset(self):
        qs = DocumentRevision.objects.all()   # même logique que votre queryset initial
        logger.debug(
            "DocumentRevision queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()           # conserve votre logique de création
        logger.info(
            "DocumentRevision créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DocumentRevisionViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\keenkonnect\knowledge_hub\urls.py

```py
# apps/keenkonnect/knowledge_hub/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.knowledge_hub.views import (
    KnowledgeDocumentViewSet,
    DocumentRevisionViewSet,
)

app_name = "knowledge_hub"

router = DefaultRouter()
router.register(r"knowledge_documents",  KnowledgeDocumentViewSet)
router.register(r"document_revisions",    DocumentRevisionViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\keenkonnect\knowledge_hub\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="KnowledgeDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the document.", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Description of the document.", null=True
                    ),
                ),
                (
                    "document_file",
                    models.FileField(
                        help_text="Uploaded document file.",
                        upload_to="knowledge_documents/",
                    ),
                ),
                (
                    "version",
                    models.CharField(
                        default="1.0", help_text="Document version.", max_length=50
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="User who created/uploaded the document.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="knowledge_documents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DocumentRevision",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "revision_number",
                    models.CharField(
                        help_text="Revision number or identifier.", max_length=50
                    ),
                ),
                (
                    "changes",
                    models.TextField(
                        help_text="Description of the changes in this revision."
                    ),
                ),
                (
                    "revised_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Timestamp when the revision was made.",
                    ),
                ),
                (
                    "revised_by",
                    models.ForeignKey(
                        help_text="User who made the revision.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="document_revisions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "knowledge_document",
                    models.ForeignKey(
                        help_text="The document to which this revision belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="revisions",
                        to="knowledge_hub.knowledgedocument",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\keenkonnect\knowledge_hub\forms.py

```py

```


---
## apps\keenkonnect\projects\apps.py

```py

```


---
## apps\keenkonnect\projects\admin.py

```py
# apps/keenkonnect/projects/admin.py

from django.contrib import admin
from keenkonnect.projects.models import Project, Milestone, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'progress', 'status', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'owner')
    search_fields = ('title', 'description')
    ordering = ('title',)
    
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} projet(s) marqué(s) comme terminé(s).")
    mark_as_completed.short_description = "Marquer les projets sélectionnés comme terminés"

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date', 'status', 'created_at')
    list_filter = ('project', 'status')
    search_fields = ('title',)
    ordering = ('project', 'due_date')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'milestone', 'assigned_to', 'is_completed', 'created_at')
    list_filter = ('milestone', 'is_completed')
    search_fields = ('title', 'description')
    ordering = ('milestone', 'title')
    
    actions = ['mark_tasks_completed']

    def mark_tasks_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f"{updated} tâche(s) marquée(s) comme complétée(s).")
    mark_tasks_completed.short_description = "Marquer les tâches sélectionnées comme complétées"

```


---
## apps\keenkonnect\projects\models.py

```py
"""
File: apps/keenkonnectprojects/models.py

This module manages the project lifecycle. It includes models for Projects,
Milestones, and Tasks for project collaboration and progress tracking.
"""

from django.db import models
from common.base_models import BaseModel

class Project(BaseModel):
    """
    Represents a collaborative project.
    """
    title = models.CharField(max_length=255, help_text="Title of the project.")
    description = models.TextField(help_text="Detailed description of the project.")
    owner = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_projects",
        help_text="User who created/owns the project."
    )
    progress = models.PositiveIntegerField(default=0, help_text="Progress percentage (0-100) of the project.")
    start_date = models.DateField(null=True, blank=True, help_text="Project start date.")
    end_date = models.DateField(null=True, blank=True, help_text="Project expected end date.")
    status = models.CharField(max_length=50, default="planning", help_text="Current status of the project.")

    def __str__(self):
        return self.title

class Milestone(BaseModel):
    """
    Represents a milestone within a project.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="milestones",
        help_text="The project to which this milestone belongs."
    )
    title = models.CharField(max_length=255, help_text="Title of the milestone.")
    description = models.TextField(null=True, blank=True, help_text="Milestone description.")
    due_date = models.DateField(null=True, blank=True, help_text="Due date for the milestone.")
    status = models.CharField(max_length=50, default="pending", help_text="Status of the milestone.")

    def __str__(self):
        return f"{self.project.title} - {self.title}"

class Task(BaseModel):
    """
    Represents a task under a milestone.
    """
    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="Milestone to which this task belongs."
    )
    title = models.CharField(max_length=255, help_text="Task title.")
    description = models.TextField(null=True, blank=True, help_text="Task description.")
    assigned_to = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
        help_text="User assigned to this task."
    )
    due_date = models.DateField(null=True, blank=True, help_text="Due date for the task.")
    is_completed = models.BooleanField(default=False, help_text="Indicates if the task is completed.")

    def __str__(self):
        status = "Completed" if self.is_completed else "Pending"
        return f"{self.title} ({status})"

```


---
## apps\keenkonnect\projects\serializers.py

```py
from rest_framework import serializers
from keenkonnect.projects.models import Project, Milestone, Task

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'owner',
            'progress',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at'
        ]

class MilestoneSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Milestone
        fields = [
            'id',
            'project',
            'title',
            'description',
            'due_date',
            'status',
            'created_at',
            'updated_at'
        ]

class TaskSerializer(serializers.ModelSerializer):
    milestone = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'milestone',
            'title',
            'description',
            'assigned_to',
            'due_date',
            'is_completed',
            'created_at',
            'updated_at'
        ]

```


---
## apps\keenkonnect\projects\views.py

```py
# apps/keenkonnect/projects/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from keenkonnect.projects.models import Project, Milestone, Task
from keenkonnect.projects.serializers import (
    ProjectSerializer,
    MilestoneSerializer,
    TaskSerializer
)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets collaboratifs.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les projets dont on est propriétaire
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Crée le projet et l'associe au propriétaire
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_status(self, request, pk=None):
        """
        Modifie le statut d'un projet (e.g. 'planning', 'in_progress', 'completed').
        """
        project = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'Le champ "status" est requis.'},
                            status=status.HTTP_400_BAD_REQUEST)
        project.status = new_status
        project.save()
        return Response(self.get_serializer(project).data)


class MilestoneViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les jalons d'un projet.
    """
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les jalons des projets dont on est propriétaire
        return Milestone.objects.filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        # S'assure que 'project' appartient bien à request.user dans le payload
        serializer.save()


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les tâches d'un jalon de projet.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les tâches des projets dont on est propriétaire
        return Task.objects.filter(milestone__project__owner=self.request.user)

    def perform_create(self, serializer):
        # On peut assigner automatiquement un utilisateur ou laisser via request.data
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_completed(self, request, pk=None):
        """
        Marque une tâche comme complétée.
        """
        task = self.get_object()
        task.is_completed = True
        task.save()
        return Response(self.get_serializer(task).data)

```


---
## apps\keenkonnect\projects\urls.py

```py
# apps/keenkonnect/projects/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.projects.views import ProjectViewSet, MilestoneViewSet, TaskViewSet

app_name = "projects"

router = DefaultRouter()
router.register(r"projects",   ProjectViewSet)
router.register(r"milestones", MilestoneViewSet)
router.register(r"tasks",      TaskViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\keenkonnect\projects\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(help_text="Title of the project.", max_length=255),
                ),
                (
                    "description",
                    models.TextField(help_text="Detailed description of the project."),
                ),
                (
                    "progress",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Progress percentage (0-100) of the project.",
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        blank=True, help_text="Project start date.", null=True
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        blank=True, help_text="Project expected end date.", null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        default="planning",
                        help_text="Current status of the project.",
                        max_length=50,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        help_text="User who created/owns the project.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="owned_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Milestone",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the milestone.", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Milestone description.", null=True
                    ),
                ),
                (
                    "due_date",
                    models.DateField(
                        blank=True, help_text="Due date for the milestone.", null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        default="pending",
                        help_text="Status of the milestone.",
                        max_length=50,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="The project to which this milestone belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="milestones",
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("title", models.CharField(help_text="Task title.", max_length=255)),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Task description.", null=True
                    ),
                ),
                (
                    "due_date",
                    models.DateField(
                        blank=True, help_text="Due date for the task.", null=True
                    ),
                ),
                (
                    "is_completed",
                    models.BooleanField(
                        default=False, help_text="Indicates if the task is completed."
                    ),
                ),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        help_text="User assigned to this task.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "milestone",
                    models.ForeignKey(
                        help_text="Milestone to which this task belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="projects.milestone",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\keenkonnect\projects\forms.py

```py

```


---
## apps\keenkonnect\team_formation\apps.py

```py
from django.apps import AppConfig

class KeenkonnectTeamFormationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keenkonnect.team_formation'
    verbose_name = "Keenkonnect Team Formation"

```


---
## apps\keenkonnect\team_formation\admin.py

```py
# apps/keenkonnect/team_formation/admin.py

from django.contrib import admin
from keenkonnect.team_formation.models import TeamFormationRequest, TeamFormationCandidate

@admin.register(TeamFormationRequest)
class TeamFormationRequestAdmin(admin.ModelAdmin):
    list_display = ('project', 'requested_by', 'created_at')
    search_fields = ('project__title', 'requested_by__username')
    ordering = ('-created_at',)
    
    actions = ['trigger_team_formation']

    def trigger_team_formation(self, request, queryset):
        # Intégrer ici l'appel à une tâche asynchrone si besoin
        count = queryset.count()
        self.message_user(request, f"Processus de formation d'équipe déclenché pour {count} demande(s).")
    trigger_team_formation.short_description = "Déclencher la formation d'équipe pour les demandes sélectionnées"

@admin.register(TeamFormationCandidate)
class TeamFormationCandidateAdmin(admin.ModelAdmin):
    list_display = ('formation_request', 'user', 'compatibility_score', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)

```


---
## apps\keenkonnect\team_formation\models.py

```py
"""
File: apps/keenkonnect/keenTeamFormation/models.py

This module defines models for AI-driven team formation.
It captures team formation requests and candidate evaluations with computed compatibility scores.
"""

from django.db import models
from common.base_models import BaseModel

class TeamFormationRequest(BaseModel):
    """
    Represents a request to form a team for a project.
    """
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="team_formation_requests",
        help_text="Project for which the team is being formed."
    )
    requested_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="team_formation_requests",
        help_text="User who initiated the team formation request."
    )
    required_roles = models.JSONField(null=True, blank=True, help_text="JSON specifying required roles and skills.")
    additional_info = models.TextField(null=True, blank=True, help_text="Additional information about the request.")

    def __str__(self):
        return f"Team Formation Request for {self.project.title}"

class TeamFormationCandidate(BaseModel):
    """
    Represents a candidate for team formation, with a computed compatibility score.
    """
    formation_request = models.ForeignKey(
        TeamFormationRequest,
        on_delete=models.CASCADE,
        related_name="candidates",
        help_text="Associated team formation request."
    )
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="team_formation_candidates",
        help_text="User being considered for the team."
    )
    skills = models.JSONField(null=True, blank=True, help_text="JSON data representing the user's skills.")
    compatibility_score = models.FloatField(default=0, help_text="Computed compatibility score.")

    def __str__(self):
        return f"Candidate {self.user} - Score: {self.compatibility_score}"

```


---
## apps\keenkonnect\team_formation\serializers.py

```py
from rest_framework import serializers
from keenkonnect.team_formation.models import TeamFormationRequest, TeamFormationCandidate

class TeamFormationRequestSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    requested_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TeamFormationRequest
        fields = [
            'id',
            'project',
            'requested_by',
            'required_roles',
            'additional_info',
            'created_at',
            'updated_at'
        ]

class TeamFormationCandidateSerializer(serializers.ModelSerializer):
    formation_request = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TeamFormationCandidate
        fields = [
            'id',
            'formation_request',
            'user',
            'skills',
            'compatibility_score',
            'created_at',
            'updated_at'
        ]

```


---
## apps\keenkonnect\team_formation\views.py

```py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from keenkonnect.team_formation.models import (
    TeamFormationRequest,
    TeamFormationCandidate
)
from keenkonnect.team_formation.serializers import (
    TeamFormationRequestSerializer,
    TeamFormationCandidateSerializer
)
# Exemple : Importer une tâche asynchrone pour lancer la formation d'équipe
# from keenkonnect.team_formation.tasks import trigger_team_formation

class TeamFormationRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les demandes de formation d'équipe.
    """
    serializer_class = TeamFormationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les demandes initiées par l'utilisateur connecté
        return TeamFormationRequest.objects.filter(requested_by=self.request.user)

    def perform_create(self, serializer):
        # Création et association automatique à l'utilisateur
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def form_team(self, request, pk=None):
        """
        Action personnalisée pour déclencher le processus de formation d'équipe.
        """
        formation_request = self.get_object()
        # Si vous utilisez Celery : trigger_team_formation.delay(formation_request.id)
        return Response({
            "status": "Processus de formation déclenché",
            "request_id": formation_request.id
        })


class TeamFormationCandidateViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les candidats à la formation d'équipe.
    """
    serializer_class = TeamFormationCandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les candidats des demandes de l'utilisateur connecté
        return TeamFormationCandidate.objects.filter(
            formation_request__requested_by=self.request.user
        )

    # Si besoin, on peut surcharger perform_create pour valider la formation_request
    # def perform_create(self, serializer):
    #     serializer.save()

```


---
## apps\keenkonnect\team_formation\urls.py

```py
# apps/keenkonnect/team_formation/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.team_formation.views import (
    TeamFormationRequestViewSet,
    TeamFormationCandidateViewSet,
)

app_name = "team_formation"

router = DefaultRouter()
router.register(r"team_formation_requests",   TeamFormationRequestViewSet)
router.register(r"team_formation_candidates", TeamFormationCandidateViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\keenkonnect\team_formation\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamFormationRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "required_roles",
                    models.JSONField(
                        blank=True,
                        help_text="JSON specifying required roles and skills.",
                        null=True,
                    ),
                ),
                (
                    "additional_info",
                    models.TextField(
                        blank=True,
                        help_text="Additional information about the request.",
                        null=True,
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        help_text="Project for which the team is being formed.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_formation_requests",
                        to="projects.project",
                    ),
                ),
                (
                    "requested_by",
                    models.ForeignKey(
                        help_text="User who initiated the team formation request.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="team_formation_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TeamFormationCandidate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "skills",
                    models.JSONField(
                        blank=True,
                        help_text="JSON data representing the user's skills.",
                        null=True,
                    ),
                ),
                (
                    "compatibility_score",
                    models.FloatField(
                        default=0, help_text="Computed compatibility score."
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User being considered for the team.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_formation_candidates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "formation_request",
                    models.ForeignKey(
                        help_text="Associated team formation request.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidates",
                        to="team_formation.teamformationrequest",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\keenkonnect\team_formation\forms.py

```py

```


---
## apps\konnaxion\ai\apps.py

```py
from django.apps import AppConfig

class KonnaxionAiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnaxion.ai'
    verbose_name = "Konnaxion AI"

```


---
## apps\konnaxion\ai\admin.py

```py
# apps/konnaxion/ai/admin.py

from django.contrib import admin
from konnaxion.ai.models import AIResult

@admin.register(AIResult)
class AIResultAdmin(admin.ModelAdmin):
    list_display = ('result_type', 'source_model', 'source_object_id', 'created_at')
    list_filter = ('result_type',)
    search_fields = ('source_model',)
    ordering = ('-created_at',)

```


---
## apps\konnaxion\ai\models.py

```py
"""
File: apps/konnaxion/ai/models.py

This module defines models for AI/ML functionalities that enhance content,
provide recommendations, and perform sentiment analysis.
"""

from django.db import models
from common.base_models import BaseModel

class AIResult(BaseModel):
    """
    Model to store AI-generated results, such as content summaries,
    translations, recommendations, and sentiment analysis.
    """
    RESULT_TYPE_CHOICES = [
        ('summary', 'Summary'),
        ('translation', 'Translation'),
        ('recommendation', 'Recommendation'),
        ('sentiment', 'Sentiment Analysis'),
    ]
    result_type = models.CharField(
        max_length=20,
        choices=RESULT_TYPE_CHOICES,
        help_text="Type of AI result."
    )
    result_data = models.JSONField(
        help_text="The AI-generated result data in JSON format."
    )
    source_model = models.CharField(
        max_length=100,
        help_text="Name of the source model (e.g., Lesson, Debate)."
    )
    source_object_id = models.PositiveIntegerField(
        help_text="ID of the source object for which the AI result was generated."
    )

    def __str__(self):
        return f"{self.get_result_type_display()} for {self.source_model} #{self.source_object_id}"

```


---
## apps\konnaxion\ai\serializers.py

```py
from rest_framework import serializers
from konnaxion.ai.models import AIResult

class AIResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIResult
        fields = [
            'id',
            'result_type',
            'result_data',
            'source_model',
            'source_object_id',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnaxion\ai\views.py

```py
# apps/konnaxion/ai/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from konnaxion.ai.models import AIResult
from konnaxion.ai.serializers import AIResultSerializer
# Exemple : Importer la tâche d’analyse IA asynchrone
# from konnaxion.ai.tasks import generate_ai_result

logger = logging.getLogger(__name__)


class AIResultViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour les résultats générés par l’IA.
    Possède une action personnalisée pour déclencher le traitement IA sur un objet source.
    """
    serializer_class = AIResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source_model', 'source_object_id', 'status']  # à ajuster selon vos champs
    search_fields = ['result']                                         # à adapter si nécessaire
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = AIResult.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "AIResult queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()  # conserve votre logique de création
        logger.info(
            "AIResult créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "AIResult mis à jour (id=%s) via API par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "AIResult supprimé (id=%s) via API par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans AIResultViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

    @action(detail=False, methods=['post'], url_path='generate', permission_classes=[permissions.IsAuthenticated])
    def generate(self, request):
        """
        Déclenche la génération d’un résultat IA pour un objet source.
        Expects 'source_model' et 'source_object_id' dans request.data.
        """
        source_model = request.data.get('source_model')
        source_object_id = request.data.get('source_object_id')
        if not source_model or not source_object_id:
            logger.warning(
                "generate manquant 'source_model' ou 'source_object_id' par %s",
                request.user
            )
            return Response(
                {"error": "Les champs 'source_model' et 'source_object_id' sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # task = generate_ai_result.delay(source_model, source_object_id)
            logger.info(
                "Génération IA déclenchée pour source_model=%s, source_object_id=%s par %s",
                source_model, source_object_id, request.user
            )
            return Response(
                {
                    "message": "Génération IA déclenchée",
                    "source_model": source_model,
                    "source_object_id": source_object_id
                },
                status=status.HTTP_202_ACCEPTED
            )
        except Exception as exc:
            logger.exception(
                "Erreur lors de generate pour %s : %s",
                request.user, exc
            )
            return Response(
                {"detail": "Impossible de déclencher la génération IA."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

```


---
## apps\konnaxion\ai\urls.py

```py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.ai.views import AIResultViewSet

app_name = 'ai'

router = DefaultRouter()
router.register(r'results', AIResultViewSet, basename='airesult')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnaxion\ai\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AIResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "result_type",
                    models.CharField(
                        choices=[
                            ("summary", "Summary"),
                            ("translation", "Translation"),
                            ("recommendation", "Recommendation"),
                            ("sentiment", "Sentiment Analysis"),
                        ],
                        help_text="Type of AI result.",
                        max_length=20,
                    ),
                ),
                (
                    "result_data",
                    models.JSONField(
                        help_text="The AI-generated result data in JSON format."
                    ),
                ),
                (
                    "source_model",
                    models.CharField(
                        help_text="Name of the source model (e.g., Lesson, Debate).",
                        max_length=100,
                    ),
                ),
                (
                    "source_object_id",
                    models.PositiveIntegerField(
                        help_text="ID of the source object for which the AI result was generated."
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnaxion\ai\forms.py

```py

```


---
## apps\konnaxion\core\apps.py

```py
from django.apps import AppConfig

class KonnaxionCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnaxion.core'
    verbose_name = "Konnaxion Core"

```


---
## apps\konnaxion\core\admin.py

```py
# apps/konnaxion/core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from konnaxion.core.models import CustomUser, SystemConfiguration, ConfigurationChangeLog

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} utilisateur(s) activé(s).")
    activate_users.short_description = "Activer les utilisateurs sélectionnés"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} utilisateur(s) désactivé(s).")
    deactivate_users.short_description = "Désactiver les utilisateurs sélectionnés"


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'created_at')
    list_filter = ('key',)
    search_fields = ('key', 'value')
    ordering = ('key',)


@admin.register(ConfigurationChangeLog)
class ConfigurationChangeLogAdmin(admin.ModelAdmin):
    list_display = ('configuration', 'old_value', 'new_value', 'changed_by', 'created_at')
    list_filter = ('configuration', 'changed_by')
    search_fields = ('configuration__key',)
    ordering = ('-created_at',)

```


---
## apps\konnaxion\core\models.py

```py
"""
File: apps/konnaxion/core/models.py

This module defines the core models for user management and system configuration.
It includes a custom user model (extending Django’s AbstractUser) and models for
system-wide settings and configuration change logging.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from common.base_models import BaseModel

class CustomUser(BaseModel, AbstractUser):
    """
    Custom user model with additional fields for roles, language preferences,
    device details, and offline synchronization metadata.
    """
    language_preference = models.CharField(
        max_length=10,
        default="en",
        help_text="User's preferred language code."
    )
    device_details = models.JSONField(
        null=True, blank=True,
        help_text="JSON field storing device-related information."
    )
    role = models.CharField(
        max_length=50,
        default="user",
        help_text="User role (e.g., user, admin, moderator)."
    )
    offline_sync_token = models.CharField(
        max_length=255,
        null=True, blank=True,
        help_text="Token for offline synchronization."
    )

    def __str__(self):
        return self.username


class SystemConfiguration(BaseModel):
    """
    Model for storing system-wide configuration settings.
    """
    key = models.CharField(
        max_length=100,
        unique=True,
        help_text="Configuration key identifier."
    )
    value = models.TextField(
        help_text="Configuration value stored as text (JSON or plain text)."
    )
    description = models.TextField(
        null=True, blank=True,
        help_text="Optional description of the configuration setting."
    )

    def __str__(self):
        return f"{self.key}: {self.value}"


class ConfigurationChangeLog(BaseModel):
    """
    Model to log configuration changes for auditing purposes.
    """
    configuration = models.ForeignKey(
        SystemConfiguration,
        on_delete=models.CASCADE,
        related_name="change_logs"
    )
    old_value = models.TextField(
        help_text="Previous configuration value."
    )
    new_value = models.TextField(
        help_text="New configuration value."
    )
    changed_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="User who made the change."
    )
    change_reason = models.TextField(
        null=True, blank=True,
        help_text="Optional reason for the change."
    )

    def __str__(self):
        return f"Change on {self.configuration.key} by {self.changed_by or 'System'}"

```


---
## apps\konnaxion\core\serializers.py

```py
from rest_framework import serializers
from konnaxion.core.models import CustomUser, SystemConfiguration, ConfigurationChangeLog

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'language_preference',
            'device_details',
            'role',
            'offline_sync_token',
            'created_at',
            'updated_at'
        ]

class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = [
            'id',
            'key',
            'value',
            'description',
            'created_at',
            'updated_at'
        ]

class ConfigurationChangeLogSerializer(serializers.ModelSerializer):
    configuration = serializers.PrimaryKeyRelatedField(read_only=True)
    changed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ConfigurationChangeLog
        fields = [
            'id',
            'configuration',
            'old_value',
            'new_value',
            'changed_by',
            'change_reason',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnaxion\core\views.py

```py
# apps/konnaxion/core/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from konnaxion.core.models import (
    CustomUser,
    SystemConfiguration,
    ConfigurationChangeLog
)
from konnaxion.core.serializers import (
    CustomUserSerializer,
    SystemConfigurationSerializer,
    ConfigurationChangeLogSerializer
)
# Exemple : Importer une tâche asynchrone pour consigner les changements de configuration
# from konnaxion.core.tasks import log_configuration_change

logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des utilisateurs (CustomUser).
    """
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'role', 'email']      # à ajuster selon vos champs
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login']
    ordering = ['-date_joined']

    def get_queryset(self):
        qs = CustomUser.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "CustomUser queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(
            "CustomUser créé (id=%s) par %s",
            user.pk, self.request.user
        )

    def perform_update(self, serializer):
        user = serializer.save()
        logger.info(
            "CustomUser mis à jour (id=%s) par %s",
            user.pk, self.request.user
        )
        return user

    def perform_destroy(self, instance):
        logger.info(
            "CustomUser supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request, pk=None):
        """
        Action personnalisée pour mettre à jour le profil utilisateur.
        (Ici, vous pouvez déclencher un événement asynchrone pour la synchronisation offline ou la notification.)
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated = serializer.save()
            # Exemple : tasks.trigger_user_update_event.delay(updated.id)
            logger.info(
                "Profil utilisateur mis à jour via update_profile (id=%s) par %s",
                updated.pk, request.user
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exc:
            logger.exception(
                "Erreur dans update_profile pour %s: %s",
                request.user, exc
            )
            return Response(
                {"detail": "Impossible de mettre à jour le profil."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CustomUserViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class SystemConfigurationViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion de la configuration système.
    Toute modification peut déclencher un enregistrement asynchrone dans l’historique.
    """
    serializer_class = SystemConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['key', 'environment']  # à ajuster selon vos champs
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = SystemConfiguration.objects.all()
        logger.debug(
            "SystemConfiguration queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        cfg = serializer.save()
        logger.info(
            "SystemConfiguration créé (id=%s) par %s",
            cfg.pk, self.request.user
        )

    def perform_update(self, serializer):
        cfg = serializer.save()
        logger.info(
            "SystemConfiguration mis à jour (id=%s) par %s",
            cfg.pk, self.request.user
        )
        # Exemple : log_configuration_change.delay(cfg.id)
        return cfg

    def perform_destroy(self, instance):
        logger.info(
            "SystemConfiguration supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans SystemConfigurationViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ConfigurationChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint en lecture seule pour consulter l’historique des modifications de configuration.
    """
    serializer_class = ConfigurationChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['configuration', 'user']
    ordering_fields = ['action_time']
    ordering = ['-action_time']

    def get_queryset(self):
        qs = ConfigurationChangeLog.objects.all()
        logger.debug(
            "ConfigurationChangeLog queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ConfigurationChangeLogViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\konnaxion\core\urls.py

```py
# apps/konnaxion/core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.core.views import (
    CustomUserViewSet,
    SystemConfigurationViewSet,
    ConfigurationChangeLogViewSet,
)

app_name = "core"

router = DefaultRouter()
router.register(r"users",                    CustomUserViewSet,             basename="customuser")
router.register(r"configurations",           SystemConfigurationViewSet,    basename="systemconfiguration")
router.register(r"configuration-changelogs", ConfigurationChangeLogViewSet, basename="configurationchangelog")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnaxion\core\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="SystemConfiguration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "key",
                    models.CharField(
                        help_text="Configuration key identifier.",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "value",
                    models.TextField(
                        help_text="Configuration value stored as text (JSON or plain text)."
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Optional description of the configuration setting.",
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "language_preference",
                    models.CharField(
                        default="en",
                        help_text="User's preferred language code.",
                        max_length=10,
                    ),
                ),
                (
                    "device_details",
                    models.JSONField(
                        blank=True,
                        help_text="JSON field storing device-related information.",
                        null=True,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        default="user",
                        help_text="User role (e.g., user, admin, moderator).",
                        max_length=50,
                    ),
                ),
                (
                    "offline_sync_token",
                    models.CharField(
                        blank=True,
                        help_text="Token for offline synchronization.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="ConfigurationChangeLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "old_value",
                    models.TextField(help_text="Previous configuration value."),
                ),
                ("new_value", models.TextField(help_text="New configuration value.")),
                (
                    "change_reason",
                    models.TextField(
                        blank=True,
                        help_text="Optional reason for the change.",
                        null=True,
                    ),
                ),
                (
                    "changed_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="User who made the change.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "configuration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="change_logs",
                        to="core.systemconfiguration",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnaxion\core\forms.py

```py

```


---
## apps\konnaxion\ekoh\apps.py

```py
from django.apps import AppConfig

class KonnaxionEkohConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnaxion.ekoh'
    verbose_name = "Ekoh"

```


---
## apps\konnaxion\ekoh\admin.py

```py
# apps/konnaxion/ekoh/admin.py

from django.contrib import admin
from konnaxion.ekoh.models import ExpertiseTag, ReputationProfile, ReputationEvent, WeightedVote

@admin.register(ExpertiseTag)
class ExpertiseTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(ReputationProfile)
class ReputationProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation_score', 'ethical_multiplier', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)

@admin.register(ReputationEvent)
class ReputationEventAdmin(admin.ModelAdmin):
    list_display = ('reputation_profile', 'event_type', 'event_value', 'timestamp')
    list_filter = ('event_type',)
    search_fields = ('reputation_profile__user__username',)
    ordering = ('-timestamp',)

@admin.register(WeightedVote)
class WeightedVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_id', 'vote_value', 'weight', 'timestamp')
    search_fields = ('target_id',)
    ordering = ('-timestamp',)

```


---
## apps\konnaxion\ekoh\models.py

```py
"""
File: apps/konnaxion/ekoh/models.py

Purpose:
Develop the reputation and ethical trust engine models, including detailed reputation
profiles, event logs, weighted voting, and expertise tags.
"""

from django.db import models
from common.base_models import BaseModel

class ExpertiseTag(BaseModel):
    """
    Represents an expertise tag that classifies a user's area of specialization.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the expertise tag")
    description = models.TextField(null=True, blank=True, help_text="Description of the expertise tag")

    def __str__(self):
        return self.name

class ReputationProfile(BaseModel):
    """
    Captures detailed reputation and ethical trust data for a user.
    """
    user = models.OneToOneField(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="reputation_profile",
        help_text="User's reputation profile"
    )
    reputation_score = models.FloatField(default=0, help_text="Overall reputation score")
    ethical_multiplier = models.FloatField(default=1.0, help_text="Multiplier used for ethical adjustments")
    expertise_tags = models.ManyToManyField(
        ExpertiseTag,
        blank=True,
        related_name="profiles",
        help_text="Expertise tags assigned to the user"
    )

    def __str__(self):
        return f"Reputation Profile for {self.user}"

class ReputationEvent(BaseModel):
    """
    Logs events that impact a user's reputation.
    """
    reputation_profile = models.ForeignKey(
        ReputationProfile,
        on_delete=models.CASCADE,
        related_name="events",
        help_text="Associated reputation profile"
    )
    event_type = models.CharField(max_length=50, help_text="Type of event (e.g., vote, contribution)")
    event_value = models.FloatField(help_text="Numerical impact of the event")
    description = models.TextField(null=True, blank=True, help_text="Context or description of the event")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When the event occurred")

    def __str__(self):
        return f"{self.event_type} event for {self.reputation_profile.user}"

class WeightedVote(BaseModel):
    """
    Records a vote cast by a user with a weight determined by reputation.
    """
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="weighted_votes",
        help_text="User casting the vote"
    )
    target_id = models.PositiveIntegerField(help_text="ID of the target (e.g., a debate argument)")
    vote_value = models.IntegerField(help_text="Vote value (e.g., +1 or -1)")
    weight = models.FloatField(help_text="Vote weight based on reputation")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the vote was cast")

    def __str__(self):
        return f"Vote by {self.user} on target {self.target_id}: {self.vote_value}"

```


---
## apps\konnaxion\ekoh\serializers.py

```py
from rest_framework import serializers
from konnaxion.ekoh.models import ExpertiseTag, ReputationProfile, ReputationEvent, WeightedVote

class ExpertiseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseTag
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at'
        ]

class ReputationProfileSerializer(serializers.ModelSerializer):
    expertise_tags = ExpertiseTagSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReputationProfile
        fields = [
            'id',
            'user',
            'reputation_score',
            'ethical_multiplier',
            'expertise_tags',
            'created_at',
            'updated_at'
        ]

class ReputationEventSerializer(serializers.ModelSerializer):
    reputation_profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReputationEvent
        fields = [
            'id',
            'reputation_profile',
            'event_type',
            'event_value',
            'description',
            'timestamp',
            'created_at',
            'updated_at'
        ]

class WeightedVoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WeightedVote
        fields = [
            'id',
            'user',
            'target_id',
            'vote_value',
            'weight',
            'timestamp',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnaxion\ekoh\views.py

```py
# apps/konnaxion/ekoh/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from konnaxion.ekoh.models import (
    ExpertiseTag,
    ReputationProfile,
    ReputationEvent,
    WeightedVote
)
from konnaxion.ekoh.serializers import (
    ExpertiseTagSerializer,
    ReputationProfileSerializer,
    ReputationEventSerializer,
    WeightedVoteSerializer
)
# Exemple : Importer une tâche pour recalculer la réputation
# from konnaxion.ekoh.tasks import recalculate_reputation

logger = logging.getLogger(__name__)


class ExpertiseTagViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour gérer les tags d'expertise.
    """
    serializer_class = ExpertiseTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []               # à ajuster (ex. 'category', 'is_active', etc.)
    search_fields = ['name']            # à adapter selon votre modèle
    ordering_fields = ['created_at']    # à ajuster si vous avez un champ date
    ordering = ['-created_at']

    def get_queryset(self):
        qs = ExpertiseTag.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "ExpertiseTag queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "ExpertiseTag créé (id=%s) par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ExpertiseTagViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ReputationProfileViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour consulter et mettre à jour le profil de réputation des utilisateurs.
    """
    serializer_class = ReputationProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user']             # à ajuster (ex. 'score_range', etc.)
    ordering_fields = ['score', 'updated_at']
    ordering = ['-score']

    def get_queryset(self):
        qs = ReputationProfile.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "ReputationProfile queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "ReputationProfile créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "ReputationProfile mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ReputationProfileViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ReputationEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints en lecture seule pour consulter les événements impactant la réputation.
    """
    serializer_class = ReputationEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'event_type']  # à ajuster selon votre modèle
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = ReputationEvent.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "ReputationEvent queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ReputationEventViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class WeightedVoteViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des votes pondérés.
    À la création d'un vote, un recalcul asynchrone de la réputation peut être déclenché.
    """
    serializer_class = WeightedVoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'target']      # à ajuster selon votre modèle
    search_fields = []                         # ex. ['comment']
    ordering_fields = ['vote_value', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = WeightedVote.objects.all()       # même logique que votre queryset initial
        logger.debug(
            "WeightedVote queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        vote = serializer.save()
        logger.info(
            "WeightedVote créé (id=%s, value=%s) par %s",
            vote.pk, vote.vote_value, self.request.user
        )
        # Exemple : Déclencher la tâche asynchrone de recalcul de réputation
        # recalculate_reputation.delay(vote.user.id, vote.target_id, vote.vote_value)

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans WeightedVoteViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\konnaxion\ekoh\urls.py

```py
# apps/konnaxion/ekoh/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.ekoh.views import (
    ExpertiseTagViewSet,
    ReputationProfileViewSet,
    ReputationEventViewSet,
    WeightedVoteViewSet,
)

app_name = "ekoh"

router = DefaultRouter()
router.register(r"expertise-tags",      ExpertiseTagViewSet,       basename="expertise-tag")
router.register(r"reputation-profiles",  ReputationProfileViewSet,   basename="reputation-profile")
router.register(r"reputation-events",    ReputationEventViewSet,     basename="reputation-event")
router.register(r"weighted-votes",       WeightedVoteViewSet,        basename="weighted-vote")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnaxion\ekoh\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ExpertiseTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the expertise tag",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Description of the expertise tag",
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ReputationProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "reputation_score",
                    models.FloatField(default=0, help_text="Overall reputation score"),
                ),
                (
                    "ethical_multiplier",
                    models.FloatField(
                        default=1.0, help_text="Multiplier used for ethical adjustments"
                    ),
                ),
                (
                    "expertise_tags",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Expertise tags assigned to the user",
                        related_name="profiles",
                        to="ekoh.expertisetag",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        help_text="User's reputation profile",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reputation_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ReputationEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "event_type",
                    models.CharField(
                        help_text="Type of event (e.g., vote, contribution)",
                        max_length=50,
                    ),
                ),
                (
                    "event_value",
                    models.FloatField(help_text="Numerical impact of the event"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Context or description of the event",
                        null=True,
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, help_text="When the event occurred"
                    ),
                ),
                (
                    "reputation_profile",
                    models.ForeignKey(
                        help_text="Associated reputation profile",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="ekoh.reputationprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="WeightedVote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "target_id",
                    models.PositiveIntegerField(
                        help_text="ID of the target (e.g., a debate argument)"
                    ),
                ),
                (
                    "vote_value",
                    models.IntegerField(help_text="Vote value (e.g., +1 or -1)"),
                ),
                (
                    "weight",
                    models.FloatField(help_text="Vote weight based on reputation"),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Timestamp when the vote was cast"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="User casting the vote",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weighted_votes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnaxion\ekoh\forms.py

```py

```


---
## apps\konnaxion\messaging\apps.py

```py
from django.apps import AppConfig

class KonnaxionMessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnaxion.messaging'
    verbose_name = "Konnaxion Messaging"

```


---
## apps\konnaxion\messaging\admin.py

```py
# apps/konnaxion/messaging/admin.py

from django.contrib import admin
from konnaxion.messaging.models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_participants', 'created_at')
    search_fields = ('participants__username',)
    ordering = ('id',)

    def display_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    display_participants.short_description = "Participants"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'is_read', 'created_at')
    list_filter = ('is_read', 'sender')
    search_fields = ('content',)
    ordering = ('-created_at',)

```


---
## apps\konnaxion\messaging\models.py

```py
"""
File: apps/konnaxion/messaging/models.py

This module defines models for real‑time and persistent messaging, including
conversation threads and individual messages.
"""

from django.db import models
from common.base_models import BaseModel

class Conversation(BaseModel):
    """
    Model representing a conversation or chat thread between users.
    """
    participants = models.ManyToManyField(
        "core.CustomUser",
        related_name='conversations',
        help_text="Users participating in this conversation."
    )
    title = models.CharField(
        max_length=255,
        null=True, blank=True,
        help_text="Optional title for the conversation."
    )

    def __str__(self):
        # Note: accessing all participants in __str__ might be heavy in some contexts.
        participant_names = ", ".join([str(user) for user in self.participants.all()])
        return f"Conversation between: {participant_names}"


class Message(BaseModel):
    """
    Model for individual messages within a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to."
    )
    sender = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="User who sent the message."
    )
    content = models.TextField(
        help_text="The text content of the message."
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Indicates if the message has been read by the recipient."
    )

    def __str__(self):
        return f"Message from {self.sender} in Conversation #{self.conversation.id}"

```


---
## apps\konnaxion\messaging\serializers.py

```py
from rest_framework import serializers
from konnaxion.messaging.models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'title',
            'created_at',
            'updated_at'
        ]

class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'conversation',
            'sender',
            'content',
            'is_read',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnaxion\messaging\views.py

```py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from konnaxion.messaging.models import Conversation, Message
from konnaxion.messaging.serializers import ConversationSerializer, MessageSerializer
# Exemple : Importer une tâche pour notifier en temps réel (WebSocket/Celery)
# from konnaxion.messaging.tasks import notify_new_message

class ConversationViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les conversations auxquelles participe l'utilisateur
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Crée la conversation et ajoute automatiquement l'utilisateur
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les messages dans les conversations de l'utilisateur
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement l'utilisateur comme expéditeur
        message = serializer.save(sender=self.request.user)
        # Exemple : notifier en temps réel
        # notify_new_message.delay(message.id)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        """
        Action personnalisée pour marquer un message comme lu.
        """
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({"status": "Message marqué comme lu"})

```


---
## apps\konnaxion\messaging\urls.py

```py
# apps/konnaxion/messaging/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.messaging.views import ConversationViewSet, MessageViewSet

app_name = "messaging"

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages",      MessageViewSet,      basename="message")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnaxion\messaging\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Conversation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        help_text="Optional title for the conversation.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        help_text="Users participating in this conversation.",
                        related_name="conversations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "content",
                    models.TextField(help_text="The text content of the message."),
                ),
                (
                    "is_read",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if the message has been read by the recipient.",
                    ),
                ),
                (
                    "conversation",
                    models.ForeignKey(
                        help_text="The conversation this message belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="messaging.conversation",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        help_text="User who sent the message.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnaxion\messaging\forms.py

```py

```


---
## apps\konnaxion\notifications\apps.py

```py
from django.apps import AppConfig

class KonnaxionNotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnaxion.notifications'
    verbose_name = "Konnaxion Notifications"

```


---
## apps\konnaxion\notifications\admin.py

```py
# apps/konnaxion/notifications/admin.py

from django.contrib import admin
from konnaxion.notifications.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('message',)
    ordering = ('-created_at',)

```


---
## apps\konnaxion\notifications\models.py

```py
"""
File: apps/konnaxion/notifications/models.py

This module defines the Notification model, which centralizes the creation and
delivery of notifications across the platform.
"""

from django.db import models
from common.base_models import BaseModel

class Notification(BaseModel):
    """
    Model for system notifications.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    sender = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sent_notifications',
        help_text="User who triggered the notification."
    )
    recipient = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who receives the notification."
    )
    message = models.TextField(
        help_text="Notification message content."
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='info',
        help_text="Type/category of notification."
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Indicates if the notification has been read."
    )

    def __str__(self):
        return f"Notification for {self.recipient} - {self.get_notification_type_display()}"

```


---
## apps\konnaxion\notifications\serializers.py

```py
from rest_framework import serializers
from konnaxion.notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    recipient = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'sender',
            'recipient',
            'message',
            'notification_type',
            'is_read',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnaxion\notifications\views.py

```py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from konnaxion.notifications.models import Notification
from konnaxion.notifications.serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les notifications du destinataire connecté
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        """
        Marquer une notification comme lue.
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "Notification marquée comme lue"})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def unread(self, request):
        """
        Retourne la liste des notifications non lues pour l'utilisateur connecté.
        """
        qs = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

```


---
## apps\konnaxion\notifications\urls.py

```py
# apps/konnaxion/notifications/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.notifications.views import NotificationViewSet

app_name = "notifications"

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnaxion\notifications\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "message",
                    models.TextField(help_text="Notification message content."),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("info", "Info"),
                            ("warning", "Warning"),
                            ("error", "Error"),
                        ],
                        default="info",
                        help_text="Type/category of notification.",
                        max_length=20,
                    ),
                ),
                (
                    "is_read",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if the notification has been read.",
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        help_text="User who receives the notification.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        help_text="User who triggered the notification.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sent_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnaxion\notifications\forms.py

```py

```


---
## apps\konnaxion\search\apps.py

```py
from django.apps import AppConfig

class KonnaxionSearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnaxion.search'
    verbose_name = "Konnaxion Search"

```


---
## apps\konnaxion\search\admin.py

```py
# apps/konnaxion/search/admin.py

from django.contrib import admin
from konnaxion.search.models import SearchIndex, SearchQueryLog

@admin.register(SearchIndex)
class SearchIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_updated')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(SearchQueryLog)
class SearchQueryLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query_text', 'results_count', 'created_at')
    list_filter = ('user',)
    search_fields = ('query_text',)
    ordering = ('-created_at',)

```


---
## apps\konnaxion\search\models.py

```py
"""
File: apps/konnaxion/search/models.py

This module defines models related to search functionality. It includes models
for managing search index configurations and logging user search queries.
"""

from django.db import models
from common.base_models import BaseModel

class SearchIndex(BaseModel):
    """
    Model for storing search index configurations.
    """
    name = models.CharField(
        max_length=255,
        help_text="Name of the search index."
    )
    settings = models.JSONField(
        null=True, blank=True,
        help_text="JSON configuration for the index."
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the index was last updated."
    )

    def __str__(self):
        return self.name


class SearchQueryLog(BaseModel):
    """
    Model for logging search queries performed by users.
    """
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="User who made the search query."
    )
    query_text = models.TextField(
        help_text="The search query entered by the user."
    )
    results_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of results returned for the query."
    )

    def __str__(self):
        return f"Query: {self.query_text[:50]}"

```


---
## apps\konnaxion\search\serializers.py

```py
from rest_framework import serializers
from konnaxion.search.models import SearchIndex, SearchQueryLog

class SearchIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchIndex
        fields = [
            'id',
            'name',
            'settings',
            'last_updated',
            'created_at',
            'updated_at'
        ]

class SearchQueryLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SearchQueryLog
        fields = [
            'id',
            'user',
            'query_text',
            'results_count',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnaxion\search\views.py

```py
from rest_framework import viewsets, permissions
from konnaxion.search.models import SearchIndex, SearchQueryLog
from konnaxion.search.serializers import SearchIndexSerializer, SearchQueryLogSerializer

class SearchIndexViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour gérer la configuration des index de recherche.
    """
    serializer_class = SearchIndexSerializer

    def get_queryset(self):
        # Tous les index, modifications réservées aux admins
        return SearchIndex.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class SearchQueryLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints en lecture seule pour consulter les journaux des requêtes de recherche.
    """
    serializer_class = SearchQueryLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les logs du user courant
        return SearchQueryLog.objects.filter(user=self.request.user)

```


---
## apps\konnaxion\search\urls.py

```py
# apps/konnaxion/search/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.search.views import SearchIndexViewSet, SearchQueryLogViewSet

app_name = "search"

router = DefaultRouter()
router.register(r'indexes',   SearchIndexViewSet,       basename='searchindex')
router.register(r'querylogs', SearchQueryLogViewSet,    basename='searchquerylog')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnaxion\search\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SearchIndex",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the search index.", max_length=255
                    ),
                ),
                (
                    "settings",
                    models.JSONField(
                        blank=True,
                        help_text="JSON configuration for the index.",
                        null=True,
                    ),
                ),
                (
                    "last_updated",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Timestamp when the index was last updated.",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SearchQueryLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "query_text",
                    models.TextField(help_text="The search query entered by the user."),
                ),
                (
                    "results_count",
                    models.PositiveIntegerField(
                        default=0, help_text="Number of results returned for the query."
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        help_text="User who made the search query.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnaxion\search\forms.py

```py

```


---
## apps\konnected\foundation\apps.py

```py
from django.apps import AppConfig

class KonnectedFoundationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnected.foundation'
    verbose_name = "Konnected Foundation"

```


---
## apps\konnected\foundation\admin.py

```py
# apps/konnected/foundation/admin.py

from django.contrib import admin
from konnected.foundation.models import KnowledgeUnit

@admin.register(KnowledgeUnit)
class KnowledgeUnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'version', 'created_at')
    list_filter = ('language', 'version')
    search_fields = ('title', 'content')
    ordering = ('title',)
    
    fieldsets = (
        (None, {'fields': ('title', 'content')}),
        ('Détails', {'fields': ('language', 'version')}),
    )

```


---
## apps\konnected\foundation\models.py

```py
"""
File: apps/konnected/foundation/models.py

This module manages the core educational content (“Knowledge Units”).
It includes models for storing rich text, multimedia, and resource attachments,
with support for versioning and audit trails.
"""

from django.db import models
from common.base_models import BaseModel

class KnowledgeUnit(BaseModel):
    """
    Represents a unit of educational content.
    """
    title = models.CharField(max_length=255, help_text="Title of the knowledge unit.")
    content = models.TextField(help_text="Rich text content of the knowledge unit.")
    attachments = models.JSONField(
        null=True,
        blank=True,
        help_text="JSON list of attachment URLs or metadata."
    )
    language = models.CharField(
        max_length=10,
        default="en",
        help_text="Language code for the content."
    )
    version = models.PositiveIntegerField(
        default=1,
        help_text="Version number of the knowledge unit."
    )

    def __str__(self):
        return self.title

```


---
## apps\konnected\foundation\serializers.py

```py
from rest_framework import serializers
from konnected.foundation.models import KnowledgeUnit

class KnowledgeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeUnit
        fields = [
            'id',
            'title',
            'content',
            'attachments',
            'language',
            'version',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnected\foundation\views.py

```py
# apps/konnected/foundation/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from konnected.foundation.models import KnowledgeUnit
from konnected.foundation.serializers import KnowledgeUnitSerializer

logger = logging.getLogger(__name__)

class KnowledgeUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les Knowledge Units (contenu éducatif de base).
    """
    serializer_class = KnowledgeUnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['topic', 'is_active']    # à ajuster selon votre modèle (ex. 'topic', 'category', 'is_active', etc.)
    search_fields = ['title', 'description']     # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = KnowledgeUnit.objects.all()          # même logique que votre queryset initial
        logger.debug(
            "KnowledgeUnit queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()              # conserve votre logique de création
        logger.info(
            "KnowledgeUnit créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans KnowledgeUnitViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\konnected\foundation\urls.py

```py
# apps/konnected/foundation/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.foundation.views import KnowledgeUnitViewSet

app_name = "foundation"

router = DefaultRouter()
router.register(r"knowledge_units", KnowledgeUnitViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnected\foundation\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="KnowledgeUnit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the knowledge unit.", max_length=255
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Rich text content of the knowledge unit."
                    ),
                ),
                (
                    "attachments",
                    models.JSONField(
                        blank=True,
                        help_text="JSON list of attachment URLs or metadata.",
                        null=True,
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        default="en",
                        help_text="Language code for the content.",
                        max_length=10,
                    ),
                ),
                (
                    "version",
                    models.PositiveIntegerField(
                        default=1, help_text="Version number of the knowledge unit."
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnected\foundation\forms.py

```py

```


---
## apps\konnected\konnectedcommunity\apps.py

```py
from django.apps import AppConfig

class KonnectedCommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnected.konnectedcommunity'
    verbose_name = "Konnected Community"

```


---
## apps\konnected\konnectedcommunity\admin.py

```py
# apps/konnected/konnectedcommunity/admin.py

from django.contrib import admin
from konnected.konnectedcommunity.models import DiscussionThread, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(DiscussionThread)
class DiscussionThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'comment_count')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    inlines = [CommentInline]

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = "Nombre de commentaires"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'short_content', 'created_at')
    list_filter = ('thread', 'author')
    search_fields = ('content',)
    ordering = ('-created_at',)

    def short_content(self, obj):
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content
    short_content.short_description = "Contenu"

```


---
## apps\konnected\konnectedcommunity\models.py

```py
"""
File: apps/konnected/konnectedcommunity/models.py

This module provides a forum for educational Q&A and discussions.
It includes models for discussion threads and nested comments.
"""

from django.db import models
from common.base_models import BaseModel

class DiscussionThread(BaseModel):
    """
    Represents a discussion thread for educational topics.
    """
    title = models.CharField(max_length=255, help_text="Title of the discussion thread.")
    content = models.TextField(help_text="Initial content or description of the thread.")
    author = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="discussion_threads",
        help_text="User who started the discussion."
    )

    def __str__(self):
        return self.title

class Comment(BaseModel):
    """
    Represents a comment on a discussion thread, supporting nested replies.
    """
    thread = models.ForeignKey(
        DiscussionThread,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The discussion thread to which this comment belongs."
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Parent comment if this is a reply; null if top-level."
    )
    author = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="User who posted the comment."
    )
    content = models.TextField(help_text="Content of the comment.")
    vote_count = models.IntegerField(
        default=0,
        help_text="Net vote count for the comment."
    )

    def __str__(self):
        return f"Comment by {self.author} on {self.thread.title}"

```


---
## apps\konnected\konnectedcommunity\serializers.py

```py
from rest_framework import serializers
from konnected.konnectedcommunity.models import DiscussionThread, Comment

class DiscussionThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionThread
        fields = [
            'id',
            'title',
            'content',
            'author',
            'created_at',
            'updated_at'
        ]

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'thread',
            'parent',
            'author',
            'content',
            'vote_count',
            'created_at',
            'updated_at',
            'replies'
        ]

    def get_replies(self, obj):
        qs = obj.replies.all()
        return CommentSerializer(qs, many=True).data

```


---
## apps\konnected\konnectedcommunity\views.py

```py
# apps/konnected/konnectedcommunity/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from konnected.konnectedcommunity.models import DiscussionThread, Comment
from konnected.konnectedcommunity.serializers import (
    DiscussionThreadSerializer,
    CommentSerializer
)
from kreative.kreativecommunity.models import CommunityPost, PostComment
from kreative.kreativecommunity.serializers import (
    CommunityPostSerializer,
    PostCommentSerializer
)

logger = logging.getLogger(__name__)


class DiscussionThreadViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les fils de discussion (forum, Q&A) dans le cadre éducatif.
    """
    serializer_class = DiscussionThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = DiscussionThread.objects.filter(is_active=True)
        logger.debug(
            "DiscussionThread queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        logger.info(
            "DiscussionThread créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DiscussionThreadViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires sur les discussions.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['thread', 'parent']
    ordering = ['created_at']

    def get_queryset(self):
        qs = Comment.objects.filter(thread__is_active=True)
        logger.debug(
            "Comment queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        logger.info(
            "Comment créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CommentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class CommunityPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les posts communautaires autour des arts.
    """
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_public', 'author__username']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = CommunityPost.objects.filter(is_public=True)
        logger.debug(
            "CommunityPost queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        logger.info(
            "CommunityPost créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CommunityPostViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class PostCommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires sur les posts communautaires.
    """
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post']
    ordering = ['created_at']

    def get_queryset(self):
        qs = PostComment.objects.filter(post__is_public=True)
        logger.debug(
            "PostComment queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        logger.info(
            "PostComment créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans PostCommentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\konnected\konnectedcommunity\urls.py

```py
from django.urls import path
from .views import (
    DiscussionThreadListView,
    DiscussionThreadDetailView,
    DiscussionThreadCreateView,
    CommentCreateView,
)

app_name = "community"

urlpatterns = [
    path("", DiscussionThreadListView.as_view(), name="thread_list"),
    path("thread/<int:pk>/", DiscussionThreadDetailView.as_view(), name="thread_detail"),
    path("thread/create/", DiscussionThreadCreateView.as_view(), name="thread_create"),
    # For posting a comment on a specific thread
    path("thread/<int:thread_pk>/comment/create/", CommentCreateView.as_view(), name="comment_create"),
]

```


---
## apps\konnected\konnectedcommunity\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscussionThread",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the discussion thread.", max_length=255
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Initial content or description of the thread."
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="User who started the discussion.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="discussion_threads",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("content", models.TextField(help_text="Content of the comment.")),
                (
                    "vote_count",
                    models.IntegerField(
                        default=0, help_text="Net vote count for the comment."
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        help_text="User who posted the comment.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        help_text="Parent comment if this is a reply; null if top-level.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="konnectedcommunity.comment",
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        help_text="The discussion thread to which this comment belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="konnectedcommunity.discussionthread",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnected\konnectedcommunity\forms.py

```py

```


---
## apps\konnected\learning\apps.py

```py
from django.apps import AppConfig

class KonnectedLearningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnected.learning'
    verbose_name = "Konnected Learning"

```


---
## apps\konnected\learning\admin.py

```py
# apps/konnected/learning/admin.py

from django.contrib import admin
from konnected.learning.models import Lesson, Quiz, Question, Answer

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'knowledge_unit', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('title',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'time_limit', 'created_at')
    list_filter = ('lesson',)
    search_fields = ('title',)
    ordering = ('title',)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ('text', 'is_correct')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'quiz', 'question_type', 'created_at')
    list_filter = ('question_type', 'quiz')
    search_fields = ('text',)
    ordering = ('quiz',)
    inlines = [AnswerInline]

    def short_text(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text
    short_text.short_description = "Question"

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'question')
    search_fields = ('text',)
    ordering = ('question',)

```


---
## apps\konnected\learning\models.py

```py
"""
File: apps/konnected/konnected_learning/models.py

This module defines models for interactive lessons, quizzes, and assessments.
It includes models for lessons, quizzes, questions, and answers.
"""

from django.db import models
from common.base_models import BaseModel

class Lesson(BaseModel):
    """
    Represents an interactive lesson.
    """
    title = models.CharField(max_length=255, help_text="Title of the lesson.")
    content = models.TextField(help_text="Lesson content, which may include rich text, images, and video links.")
    # Optionally associate a lesson with a knowledge unit.
    knowledge_unit = models.ForeignKey(
        "foundation.KnowledgeUnit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
        help_text="Associated knowledge unit, if any."
    )

    def __str__(self):
        return self.title

class Quiz(BaseModel):
    """
    Represents a quiz associated with a lesson.
    """
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="quizzes",
        help_text="Lesson associated with this quiz."
    )
    title = models.CharField(max_length=255, help_text="Title of the quiz.")
    instructions = models.TextField(help_text="Quiz instructions or guidelines.")
    time_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Time limit in minutes, if applicable."
    )

    def __str__(self):
        return f"{self.title} (Quiz for {self.lesson.title})"

class Question(BaseModel):
    """
    Represents a question in a quiz.
    """
    QUESTION_TYPE_CHOICES = [
        ('text', 'Text'),
        ('multiple_choice', 'Multiple Choice'),
    ]
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="Quiz to which this question belongs."
    )
    text = models.TextField(help_text="The question text.")
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='text',
        help_text="Type of question."
    )
    correct_answer = models.TextField(
        null=True,
        blank=True,
        help_text="Correct answer for the question (if applicable)."
    )

    def __str__(self):
        return f"Question: {self.text[:50]}..."

class Answer(BaseModel):
    """
    Represents an answer option for a multiple choice question.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        help_text="The question this answer belongs to."
    )
    text = models.TextField(help_text="Answer option text.")
    is_correct = models.BooleanField(
        default=False,
        help_text="Indicates if this is the correct answer."
    )

    def __str__(self):
        return f"Answer: {self.text[:50]}{' (Correct)' if self.is_correct else ''}"

```


---
## apps\konnected\learning\serializers.py

```py
from rest_framework import serializers
from konnected.learning.models import Lesson, Quiz, Question, Answer

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'content',
            'knowledge_unit',
            'created_at',
            'updated_at'
        ]

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = [
            'id',
            'lesson',
            'title',
            'instructions',
            'time_limit',
            'created_at',
            'updated_at'
        ]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'quiz',
            'text',
            'question_type',
            'correct_answer',
            'created_at',
            'updated_at'
        ]

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'text',
            'is_correct',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnected\learning\views.py

```py
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser
from konnected.learning.models import Lesson, Quiz, Question, Answer
from konnected.learning.serializers import (
    LessonSerializer,
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer
)

class LessonViewSet(viewsets.ModelViewSet):
    """
    Gère les leçons interactives.
    Lecture pour tout utilisateur authentifié, écriture réservée aux admins.
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]


class QuizViewSet(viewsets.ModelViewSet):
    """
    Gère les quiz associés aux leçons.
    Lecture pour tout utilisateur authentifié, écriture réservée aux admins.
    """
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Gère les questions des quiz.
    Lecture pour tout utilisateur authentifié, écriture réservée aux admins.
    """
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdminUser()]


class AnswerViewSet(viewsets.ModelViewSet):
    """
    Gère les réponses aux questions.
    Chaque réponse est liée à l'utilisateur connecté.
    """
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Answer.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

```


---
## apps\konnected\learning\urls.py

```py
# apps/konnected/learning/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.learning.views import (
    LessonViewSet,
    QuizViewSet,
    QuestionViewSet,
    AnswerViewSet,
)

app_name = "learning"

router = DefaultRouter()
router.register(r"lessons",   LessonViewSet)
router.register(r"quizzes",   QuizViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"answers",   AnswerViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnected\learning\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("foundation", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("text", models.TextField(help_text="The question text.")),
                (
                    "question_type",
                    models.CharField(
                        choices=[
                            ("text", "Text"),
                            ("multiple_choice", "Multiple Choice"),
                        ],
                        default="text",
                        help_text="Type of question.",
                        max_length=20,
                    ),
                ),
                (
                    "correct_answer",
                    models.TextField(
                        blank=True,
                        help_text="Correct answer for the question (if applicable).",
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(help_text="Title of the lesson.", max_length=255),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="Lesson content, which may include rich text, images, and video links."
                    ),
                ),
                (
                    "knowledge_unit",
                    models.ForeignKey(
                        blank=True,
                        help_text="Associated knowledge unit, if any.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="lessons",
                        to="foundation.knowledgeunit",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("text", models.TextField(help_text="Answer option text.")),
                (
                    "is_correct",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if this is the correct answer.",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        help_text="The question this answer belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="learning.question",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Quiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(help_text="Title of the quiz.", max_length=255),
                ),
                (
                    "instructions",
                    models.TextField(help_text="Quiz instructions or guidelines."),
                ),
                (
                    "time_limit",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Time limit in minutes, if applicable.",
                        null=True,
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        help_text="Lesson associated with this quiz.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quizzes",
                        to="learning.lesson",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="question",
            name="quiz",
            field=models.ForeignKey(
                help_text="Quiz to which this question belongs.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="learning.quiz",
            ),
        ),
    ]

```


---
## apps\konnected\learning\forms.py

```py

```


---
## apps\konnected\offline\apps.py

```py
from django.apps import AppConfig

class KonnectedOfflineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnected.offline'
    verbose_name = "Konnected Offline"

```


---
## apps\konnected\offline\admin.py

```py
# apps/konnected/offline/admin.py

from django.contrib import admin
from django.contrib import messages
from konnected.offline.models import OfflineContentPackage

@admin.register(OfflineContentPackage)
class OfflineContentPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_synced', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    actions = ['trigger_sync']

    def trigger_sync(self, request, queryset):
        # Ici, vous pouvez intégrer l'appel à une tâche asynchrone par exemple via Celery.
        # Pour l'instant, nous simulons simplement l'action avec un message.
        count = queryset.count()
        # Exemple d'appel : sync_offline_content.delay(package.id) pour chaque package
        self.message_user(request, f"Sync déclenché pour {count} package(s).", messages.SUCCESS)
    trigger_sync.short_description = "Déclencher la synchronisation des packages offline"

```


---
## apps\konnected\offline\models.py

```py
"""
File: apps/konnected/offline/models.py

This module ensures that educational content is available offline.
It includes models for packaging content for offline consumption and tracking synchronization.
"""

from django.db import models
from common.base_models import BaseModel

class OfflineContentPackage(BaseModel):
    """
    Represents a packaged set of educational content for offline use.
    """
    title = models.CharField(max_length=255, help_text="Title of the offline content package.")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the offline package."
    )
    content_data = models.JSONField(help_text="JSON data representing the packaged content for offline use.")
    last_synced = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of the last successful sync."
    )
    conflict_resolution_notes = models.TextField(
        null=True,
        blank=True,
        help_text="Notes on any conflicts during sync."
    )

    def __str__(self):
        return self.title

```


---
## apps\konnected\offline\serializers.py

```py
from rest_framework import serializers
from konnected.offline.models import OfflineContentPackage

class OfflineContentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineContentPackage
        fields = [
            'id',
            'title',
            'description',
            'content_data',
            'last_synced',
            'conflict_resolution_notes',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnected\offline\views.py

```py
# apps/konnected/offline/views.py

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from konnected.offline.models import OfflineContentPackage
from konnected.offline.serializers import OfflineContentPackageSerializer
# Exemple : depuis un module de tâches asynchrones pour lancer la synchronisation
# from konnected.offline.tasks import sync_offline_content

class OfflineContentPackageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les packages de contenu pour l'utilisation offline.
    """
    queryset = OfflineContentPackage.objects.all()
    serializer_class = OfflineContentPackageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def sync(self, request, pk=None):
        """
        Action personnalisée pour déclencher la synchronisation du package offline.
        """
        package = self.get_object()
        # Exemple : déclencher la tâche asynchrone de synchronisation
        # sync_offline_content.delay(package.id)
        return Response({
            "status": "Sync déclenché",
            "package_id": package.id
        })

```


---
## apps\konnected\offline\urls.py

```py
# apps/konnected/offline/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.offline.views import OfflineContentPackageViewSet

app_name = "offline"

router = DefaultRouter()
router.register(r"offline_packages", OfflineContentPackageViewSet, basename="offlinepackage")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnected\offline\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OfflineContentPackage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the offline content package.",
                        max_length=255,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Description of the offline package.",
                        null=True,
                    ),
                ),
                (
                    "content_data",
                    models.JSONField(
                        help_text="JSON data representing the packaged content for offline use."
                    ),
                ),
                (
                    "last_synced",
                    models.DateTimeField(
                        blank=True,
                        help_text="Timestamp of the last successful sync.",
                        null=True,
                    ),
                ),
                (
                    "conflict_resolution_notes",
                    models.TextField(
                        blank=True,
                        help_text="Notes on any conflicts during sync.",
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnected\offline\forms.py

```py

```


---
## apps\konnected\paths\apps.py

```py
from django.apps import AppConfig

class KonnectedPathsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnected.paths'
    verbose_name = "Konnected Paths"

```


---
## apps\konnected\paths\admin.py

```py
# apps/konnected/paths/admin.py

from django.contrib import admin
from konnected.paths.models import LearningPath, PathStep

class PathStepInline(admin.TabularInline):
    model = PathStep
    extra = 1
    fields = ('knowledge_unit', 'order')

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('title',)
    inlines = [PathStepInline]

@admin.register(PathStep)
class PathStepAdmin(admin.ModelAdmin):
    list_display = ('learning_path', 'knowledge_unit', 'order')
    list_filter = ('learning_path',)
    ordering = ('learning_path', 'order')

```


---
## apps\konnected\paths\models.py

```py
"""
File: apps/konnected/paths/models.py

This module enables the creation of adaptive learning paths.
It includes models for assembling knowledge units into personalized curricula.
"""

from django.db import models
from common.base_models import BaseModel

class LearningPath(BaseModel):
    """
    Represents a personalized learning path (curriculum).
    """
    title = models.CharField(max_length=255, help_text="Title of the learning path.")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the learning path."
    )
    created_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who created the learning path."
    )

    def __str__(self):
        return self.title

class PathStep(BaseModel):
    """
    Represents an individual step within a learning path, linking a knowledge unit.
    """
    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name="steps",
        help_text="The learning path this step belongs to."
    )
    knowledge_unit = models.ForeignKey(
        "foundation.KnowledgeUnit",
        on_delete=models.CASCADE,
        related_name="path_steps",
        help_text="The knowledge unit associated with this step."
    )
    order = models.PositiveIntegerField(help_text="The order/sequence of this step in the learning path.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.learning_path.title} - Step {self.order}: {self.knowledge_unit.title}"

```


---
## apps\konnected\paths\serializers.py

```py
from rest_framework import serializers
from konnected.paths.models import LearningPath, PathStep

class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPath
        fields = [
            'id',
            'title',
            'description',
            'created_by',
            'created_at',
            'updated_at'
        ]

class PathStepSerializer(serializers.ModelSerializer):
    learning_path = serializers.PrimaryKeyRelatedField(read_only=True)
    knowledge_unit = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PathStep
        fields = [
            'id',
            'learning_path',
            'knowledge_unit',
            'order',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnected\paths\views.py

```py
# apps/konnected/paths/views.py
from rest_framework import viewsets, permissions
from konnected.paths.models import LearningPath, PathStep
from konnected.paths.serializers import (
    LearningPathSerializer,
    PathStepSerializer
)

class LearningPathViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer la création et la modification des parcours d'apprentissage.
    """
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les parcours créés par l'utilisateur connecté
        return LearningPath.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement le créateur
        serializer.save(created_by=self.request.user)


class PathStepViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les étapes individuelles d'un parcours d'apprentissage.
    """
    serializer_class = PathStepSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les étapes des parcours de l'utilisateur
        return PathStep.objects.filter(
            learning_path__created_by=self.request.user
        )

    def perform_create(self, serializer):
        # On suppose que 'learning_path' est fourni dans request.data
        serializer.save()

```


---
## apps\konnected\paths\urls.py

```py
# apps/konnected/paths/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.paths.views import LearningPathViewSet, PathStepViewSet

app_name = "paths"

router = DefaultRouter()
router.register(r"learning_paths", LearningPathViewSet)
router.register(r"path_steps",     PathStepViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnected\paths\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("foundation", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LearningPath",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the learning path.", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Description of the learning path.",
                        null=True,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        help_text="User who created the learning path.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PathStep",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "order",
                    models.PositiveIntegerField(
                        help_text="The order/sequence of this step in the learning path."
                    ),
                ),
                (
                    "knowledge_unit",
                    models.ForeignKey(
                        help_text="The knowledge unit associated with this step.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="path_steps",
                        to="foundation.knowledgeunit",
                    ),
                ),
                (
                    "learning_path",
                    models.ForeignKey(
                        help_text="The learning path this step belongs to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="steps",
                        to="paths.learningpath",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]

```


---
## apps\konnected\paths\forms.py

```py

```


---
## apps\konnected\team\apps.py

```py
from django.apps import AppConfig

class KonnectedTeamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'konnected.team'
    verbose_name = "Konnected Team"

```


---
## apps\konnected\team\admin.py

```py
# apps/konnected/team/admin.py

from django.contrib import admin
from konnected.team.models import Team, TeamInvitation

class TeamInvitationInline(admin.TabularInline):
    model = TeamInvitation
    extra = 0
    fields = ('invited_user', 'status', 'created_at')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'member_count', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [TeamInvitationInline]

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = "Nombre de membres"

@admin.register(TeamInvitation)
class TeamInvitationAdmin(admin.ModelAdmin):
    list_display = ('team', 'invited_user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('team__name', 'invited_user__username')
    ordering = ('-created_at',)

```


---
## apps\konnected\team\models.py

```py
"""
File: apps/konnected/team/models.py

This module facilitates team creation and management for educational projects.
It includes models for teams and team invitations.
"""

from django.db import models
from common.base_models import BaseModel

class Team(BaseModel):
    """
    Represents an educational team.
    """
    name = models.CharField(max_length=255, help_text="Name of the team.")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the team."
    )
    members = models.ManyToManyField(
        "core.CustomUser",
        related_name="teams",
        help_text="Users who are members of this team."
    )

    def __str__(self):
        return self.name

class TeamInvitation(BaseModel):
    """
    Represents an invitation for a user to join a team.
    """
    INVITATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="invitations",
        help_text="Team for which the invitation is sent."
    )
    invited_user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="team_invitations",
        help_text="User who is invited."
    )
    status = models.CharField(
        max_length=20,
        choices=INVITATION_STATUS_CHOICES,
        default="pending",
        help_text="Status of the invitation."
    )
    message = models.TextField(
        null=True,
        blank=True,
        help_text="Optional message accompanying the invitation."
    )

    def __str__(self):
        return f"Invitation for {self.invited_user} to join {self.team.name} [{self.status}]"

```


---
## apps\konnected\team\serializers.py

```py
from rest_framework import serializers
from konnected.team.models import Team, TeamInvitation

class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'description',
            'members',
            'created_at',
            'updated_at'
        ]

class TeamInvitationSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(read_only=True)
    invited_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TeamInvitation
        fields = [
            'id',
            'team',
            'invited_user',
            'status',
            'message',
            'created_at',
            'updated_at'
        ]

```


---
## apps\konnected\team\views.py

```py
from rest_framework import viewsets, permissions
from konnected.team.models import Team, TeamInvitation
from konnected.team.serializers import (
    TeamSerializer,
    TeamInvitationSerializer
)

class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer la création et la gestion des équipes éducatives.
    """
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les équipes où l'utilisateur est membre
        return Team.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        # Création + ajout automatique du créateur dans les membres
        team = serializer.save()
        team.members.add(self.request.user)


class TeamInvitationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les invitations à rejoindre une équipe.
    """
    serializer_class = TeamInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les invitations qui concernent l'utilisateur connecté
        return TeamInvitation.objects.filter(invited_user=self.request.user)

```


---
## apps\konnected\team\urls.py

```py
# apps/konnected/team/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.team.views import TeamViewSet, TeamInvitationViewSet

app_name = "team"

router = DefaultRouter()
router.register(r"teams",       TeamViewSet)
router.register(r"invitations", TeamInvitationViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\konnected\team\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "name",
                    models.CharField(help_text="Name of the team.", max_length=255),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Description of the team.", null=True
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        help_text="Users who are members of this team.",
                        related_name="teams",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TeamInvitation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        help_text="Status of the invitation.",
                        max_length=20,
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        blank=True,
                        help_text="Optional message accompanying the invitation.",
                        null=True,
                    ),
                ),
                (
                    "invited_user",
                    models.ForeignKey(
                        help_text="User who is invited.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_invitations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        help_text="Team for which the invitation is sent.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invitations",
                        to="team.team",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\konnected\team\forms.py

```py

```


---
## apps\kreative\artworks\apps.py

```py
from django.apps import AppConfig

class KreativeArtworksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kreative.artworks'
    verbose_name = "Kreative Artworks"

```


---
## apps\kreative\artworks\admin.py

```py
# apps/kreative/artworks/admin.py

from django.contrib import admin
from kreative.artworks.models import Exhibition, Artwork
from django.utils.html import mark_safe

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location', 'created_at')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'description', 'location')
    ordering = ('-start_date',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Détails de l\'exposition', {
            'fields': ('start_date', 'end_date', 'location')
        }),
    )

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'exhibition', 'created_at', 'image_tag')
    list_filter = ('exhibition',)
    search_fields = ('title', 'description')
    ordering = ('title',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'exhibition')
        }),
        ('Image', {
            'fields': ('image',),
        }),
    )
    
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return ""
    image_tag.short_description = "Image"

```


---
## apps\kreative\artworks\models.py

```py
"""
File: apps\kreative\artworks\models.py

Purpose:
Build models for the artwork catalog, including fields for media uploads, metadata,
and exhibition details.
"""

from django.db import models
from common.base_models import BaseModel

class Exhibition(BaseModel):
    """
    Represents an exhibition event for displaying artworks.
    """
    name = models.CharField(max_length=255, help_text="Name of the exhibition")
    description = models.TextField(null=True, blank=True, help_text="Description of the exhibition")
    start_date = models.DateField(null=True, blank=True, help_text="Exhibition start date")
    end_date = models.DateField(null=True, blank=True, help_text="Exhibition end date")
    location = models.CharField(max_length=255, null=True, blank=True, help_text="Location of the exhibition")

    def __str__(self):
        return self.name

class Artwork(BaseModel):
    """
    Represents an individual artwork in the catalog.
    """
    title = models.CharField(max_length=255, help_text="Title of the artwork")
    description = models.TextField(help_text="Description of the artwork")
    image = models.ImageField(upload_to="artworks/", help_text="Image of the artwork")
    metadata = models.JSONField(null=True, blank=True, help_text="Additional metadata (e.g., dimensions, medium)")
    exhibition = models.ForeignKey(
        Exhibition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artworks",
        help_text="Exhibition where the artwork is displayed"
    )

    def __str__(self):
        return self.title

```


---
## apps\kreative\artworks\serializers.py

```py
from rest_framework import serializers
from kreative.artworks.models import Exhibition, Artwork

class ExhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
            'location',
            'created_at',
            'updated_at'
        ]

class ArtworkSerializer(serializers.ModelSerializer):
    exhibition = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Artwork
        fields = [
            'id',
            'title',
            'description',
            'image',
            'metadata',
            'exhibition',
            'created_at',
            'updated_at'
        ]

```


---
## apps\kreative\artworks\views.py

```py
# apps/kreative/artworks/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from kreative.artworks.models import Exhibition, Artwork
from kreative.artworks.serializers import ExhibitionSerializer, ArtworkSerializer

logger = logging.getLogger(__name__)


class ExhibitionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les expositions (création, modification, suppression et consultation).
    """
    serializer_class = ExhibitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active', 'location']      # ajuster selon vos champs réels
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-start_date']

    def get_queryset(self):
        qs = Exhibition.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "Exhibition queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "Exhibition créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "Exhibition mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "Exhibition supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def activate(self, request, pk=None):
        """
        Action personnalisée pour activer/désactiver une exposition.
        Attendu : un booléen 'active' dans request.data.
        """
        exhibition = self.get_object()
        active = request.data.get('active')
        if active is None:
            logger.warning("activate sans paramètre 'active' par %s", request.user)
            return Response(
                {"error": "Le champ 'active' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            exhibition.active = bool(active)
            exhibition.save()
            logger.info(
                "Exhibition (id=%s) active=%s mise à jour par %s",
                exhibition.pk, exhibition.active, request.user
            )
            return Response(
                self.get_serializer(exhibition).data,
                status=status.HTTP_200_OK
            )
        except Exception as exc:
            logger.exception(
                "Erreur dans activate pour Exhibition id=%s par %s: %s",
                exhibition.pk, request.user, exc
            )
            return Response(
                {"detail": "Impossible de changer le statut de l'exposition."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ExhibitionViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ArtworkViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer le catalogue des œuvres.
    """
    serializer_class = ArtworkSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['exhibition', 'artist']    # ajuster selon vos champs
    search_fields = ['title', 'medium']
    ordering_fields = ['created_at', 'year']
    ordering = ['created_at']

    def get_queryset(self):
        qs = Artwork.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "Artwork queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "Artwork créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "Artwork mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "Artwork supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def by_exhibition(self, request):
        """
        Retourne la liste des œuvres filtrées par l'exposition.
        Expects : un paramètre 'exhibition_id' dans les query params.
        """
        exhibition_id = request.query_params.get('exhibition_id')
        qs = self.get_queryset()
        if exhibition_id:
            qs = qs.filter(exhibition_id=exhibition_id)
        logger.debug(
            "by_exhibition: %d artworks pour exhibition_id=%s par %s",
            qs.count(), exhibition_id, request.user
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ArtworkViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\kreative\artworks\urls.py

```py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kreative.artworks.views import ExhibitionViewSet, ArtworkViewSet

app_name = 'artworks'

router = DefaultRouter()
router.register(r'exhibitions', ExhibitionViewSet, basename='exhibition')
router.register(r'artworks', ArtworkViewSet, basename='artwork')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\kreative\artworks\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Exhibition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the exhibition", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Description of the exhibition", null=True
                    ),
                ),
                (
                    "start_date",
                    models.DateField(
                        blank=True, help_text="Exhibition start date", null=True
                    ),
                ),
                (
                    "end_date",
                    models.DateField(
                        blank=True, help_text="Exhibition end date", null=True
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True,
                        help_text="Location of the exhibition",
                        max_length=255,
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Artwork",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(help_text="Title of the artwork", max_length=255),
                ),
                (
                    "description",
                    models.TextField(help_text="Description of the artwork"),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Image of the artwork", upload_to="artworks/"
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True,
                        help_text="Additional metadata (e.g., dimensions, medium)",
                        null=True,
                    ),
                ),
                (
                    "exhibition",
                    models.ForeignKey(
                        blank=True,
                        help_text="Exhibition where the artwork is displayed",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="artworks",
                        to="artworks.exhibition",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\kreative\artworks\forms.py

```py

```


---
## apps\kreative\immersive\apps.py

```py
from django.apps import AppConfig

class KreativeImmersiveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kreative.immersive'
    verbose_name = "Kreative Immersive"

```


---
## apps\kreative\immersive\admin.py

```py
# apps/kreative/immersive/admin.py

from django.contrib import admin
from kreative.immersive.models import ImmersiveExperience

@admin.register(ImmersiveExperience)
class ImmersiveExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_url', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Contenu Immersif', {'fields': ('media_url',)}),
    )

```


---
## apps\kreative\immersive\models.py

```py
"""
File: apps/kreative/kreative_immersive/models.py

Purpose:
(Optional/Future) Define minimal placeholder models to support AR/VR and immersive cultural experiences.
"""

from django.db import models
from common.base_models import BaseModel

class ImmersiveExperience(BaseModel):
    """
    Placeholder model for AR/VR and immersive cultural experiences.
    """
    title = models.CharField(max_length=255, help_text="Title of the immersive experience")
    description = models.TextField(help_text="Description of the immersive experience")
    media_url = models.URLField(null=True, blank=True, help_text="URL for the immersive AR/VR content")

    def __str__(self):
        return self.title

```


---
## apps\kreative\immersive\serializers.py

```py
from rest_framework import serializers
from kreative.immersive.models import ImmersiveExperience

class ImmersiveExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmersiveExperience
        fields = [
            'id',
            'title',
            'description',
            'media_url',
            'created_at',
            'updated_at'
        ]

```


---
## apps\kreative\immersive\views.py

```py
# apps/kreative/immersive/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from kreative.immersive.models import ImmersiveExperience
from kreative.immersive.serializers import ImmersiveExperienceSerializer

logger = logging.getLogger(__name__)

class ImmersiveExperienceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les expériences immersives (AR/VR).
    Ce module est minimal et peut être étendu ultérieurement.
    """
    serializer_class = ImmersiveExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []                       # à ajuster selon vos champs (ex. 'category', 'is_active', etc.)
    search_fields = ['title', 'description']    # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = ImmersiveExperience.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "ImmersiveExperience queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()            # conserve votre logique de création
        logger.info(
            "ImmersiveExperience créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ImmersiveExperienceViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\kreative\immersive\urls.py

```py
# apps/kreative/immersive/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kreative.immersive.views import ImmersiveExperienceViewSet

app_name = "immersive"

router = DefaultRouter()
router.register(r"immersive_experiences", ImmersiveExperienceViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\kreative\immersive\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ImmersiveExperience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the immersive experience", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Description of the immersive experience"
                    ),
                ),
                (
                    "media_url",
                    models.URLField(
                        blank=True,
                        help_text="URL for the immersive AR/VR content",
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\kreative\immersive\forms.py

```py

```


---
## apps\kreative\kreativecommunity\apps.py

```py
from django.apps import AppConfig

class KreativeCommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kreative.kreativecommunity'
    verbose_name = "Kreative Community"

```


---
## apps\kreative\kreativecommunity\admin.py

```py
# apps/kreative/community/admin.py

from django.contrib import admin
from kreative.kreativecommunity.models import CommunityPost, PostComment

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('title', 'content')}),
        ('Informations', {'fields': ('posted_by',)}),
    )

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'commented_by', 'short_content', 'created_at')
    list_filter = ('post', 'commented_by')
    search_fields = ('content',)
    ordering = ('-created_at',)
    
    def short_content(self, obj):
        return (obj.content[:75] + '...') if len(obj.content) > 75 else obj.content
    short_content.short_description = "Contenu"

```


---
## apps\kreative\kreativecommunity\models.py

```py
"""
File: apps/kreative/kreative_community/models.py

Purpose:
Create models for community posts, reviews, ratings, and threaded comments related to art.
"""

from django.db import models
from common.base_models import BaseModel

class CommunityPost(BaseModel):
    """
    Represents a community post related to art.
    """
    title = models.CharField(max_length=255, help_text="Title of the post")
    content = models.TextField(help_text="Content of the post")
    posted_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="community_posts",
        help_text="User who posted the community post"
    )

    def __str__(self):
        return self.title

class PostComment(BaseModel):
    """
    Represents a comment on a community post, supporting threaded replies.
    """
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The community post being commented on"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Parent comment for threaded replies"
    )
    content = models.TextField(help_text="Content of the comment")
    commented_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="post_comments",
        help_text="User who made the comment"
    )

    def __str__(self):
        return f"Comment by {self.commented_by} on {self.post.title}"

class ArtworkReview(BaseModel):
    """
    Represents a review or rating for an artwork.
    """
    artwork = models.ForeignKey(
        "artworks.Artwork",
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Artwork being reviewed"
    )
    reviewed_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="artwork_reviews",
        help_text="User who reviewed the artwork"
    )
    rating = models.PositiveSmallIntegerField(help_text="Rating value (e.g., 1 to 5)")
    review_text = models.TextField(null=True, blank=True, help_text="Optional review text")

    def __str__(self):
        return f"Review for {self.artwork.title} by {self.reviewed_by}"

```


---
## apps\kreative\kreativecommunity\serializers.py

```py
from rest_framework import serializers
from kreative.kreativecommunity.models import CommunityPost, PostComment, ArtworkReview

class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = [
            'id',
            'title',
            'content',
            'posted_by',
            'created_at',
            'updated_at'
        ]

class PostCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = [
            'id',
            'post',
            'parent',
            'content',
            'commented_by',
            'created_at',
            'updated_at',
            'replies'
        ]

    def get_replies(self, obj):
        qs = obj.replies.all()
        return PostCommentSerializer(qs, many=True).data

class ArtworkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkReview
        fields = [
            'id',
            'artwork',
            'reviewed_by',
            'rating',
            'review_text',
            'created_at',
            'updated_at'
        ]

```


---
## apps\kreative\kreativecommunity\views.py

```py
# apps/konnected/konnectedcommunity/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from konnected.konnectedcommunity.models import DiscussionThread, Comment
from konnected.konnectedcommunity.serializers import (
    DiscussionThreadSerializer,
    CommentSerializer
)

logger = logging.getLogger(__name__)

class DiscussionThreadViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les fils de discussion (forum, Q&A) dans le cadre éducatif.
    """
    serializer_class = DiscussionThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']          # à ajuster selon vos champs
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = DiscussionThread.objects.all()       # même logique que votre queryset initial
        logger.debug(
            "DiscussionThread queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()               # conserve votre logique de création
        logger.info(
            "DiscussionThread créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DiscussionThreadViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires sur les discussions.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['thread']                 # à ajuster si besoin
    ordering = ['created_at']

    def get_queryset(self):
        qs = Comment.objects.all()                # même logique que votre queryset initial
        logger.debug(
            "Comment queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()               # conserve votre logique de création
        logger.info(
            "Comment créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CommentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

```


---
## apps\kreative\kreativecommunity\urls.py

```py
# apps/konnected/community/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.konnectedcommunity.views import DiscussionThreadViewSet, CommentViewSet

app_name = "community"

router = DefaultRouter()
router.register(r"discussions", DiscussionThreadViewSet)
router.register(r"comments",    CommentViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\kreative\kreativecommunity\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("artworks", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtworkReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        help_text="Rating value (e.g., 1 to 5)"
                    ),
                ),
                (
                    "review_text",
                    models.TextField(
                        blank=True, help_text="Optional review text", null=True
                    ),
                ),
                (
                    "artwork",
                    models.ForeignKey(
                        help_text="Artwork being reviewed",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="artworks.artwork",
                    ),
                ),
                (
                    "reviewed_by",
                    models.ForeignKey(
                        help_text="User who reviewed the artwork",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="artwork_reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CommunityPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(help_text="Title of the post", max_length=255),
                ),
                ("content", models.TextField(help_text="Content of the post")),
                (
                    "posted_by",
                    models.ForeignKey(
                        help_text="User who posted the community post",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="community_posts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PostComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("content", models.TextField(help_text="Content of the comment")),
                (
                    "commented_by",
                    models.ForeignKey(
                        help_text="User who made the comment",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        help_text="Parent comment for threaded replies",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="kreativecommunity.postcomment",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        help_text="The community post being commented on",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="kreativecommunity.communitypost",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\kreative\kreativecommunity\forms.py

```py

```


---
## apps\kreative\marketplace\apps.py

```py
from django.apps import AppConfig

class KreativeMarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kreative.marketplace'
    verbose_name = "Kreative Marketplace"

```


---
## apps\kreative\marketplace\admin.py

```py
# apps/kreative/marketplace/admin.py

from django.contrib import admin
from kreative.marketplace.models import ArtistProfile, Commission, MarketplaceListing

@admin.register(ArtistProfile)
class ArtistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio_url', 'created_at')
    search_fields = ('user__username', 'portfolio_url')
    ordering = ('-created_at',)

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'requested_by', 'status', 'budget', 'created_at')
    list_filter = ('status', 'requested_by')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    
    actions = ['change_status']
    
    def change_status(self, request, queryset):
        new_status = request.POST.get('new_status')
        if new_status:
            updated = queryset.update(status=new_status)
            self.message_user(request, f"{updated} commission(s) mise(s) à jour avec le statut {new_status}.")
        else:
            self.message_user(request, "Veuillez spécifier un nouveau statut.", level='error')
    change_status.short_description = "Changer le statut des commissions sélectionnées"

@admin.register(MarketplaceListing)
class MarketplaceListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist_profile', 'price', 'status', 'created_at')
    list_filter = ('status', 'artist_profile')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

```


---
## apps\kreative\marketplace\models.py

```py
"""
File: apps/kreative/kreative_marketplace/models.py

Purpose:
Develop models for managing commissions, artist profiles, and marketplace listings.
Optionally includes placeholders for payment or contract integration.
"""

from django.db import models
from common.base_models import BaseModel

class ArtistProfile(BaseModel):
    """
    Represents an artist's profile containing portfolio and biography details.
    """
    user = models.OneToOneField(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="artist_profile",
        help_text="Associated user for the artist profile"
    )
    biography = models.TextField(null=True, blank=True, help_text="Artist biography")
    portfolio_url = models.URLField(null=True, blank=True, help_text="URL to the artist's portfolio")
    metadata = models.JSONField(null=True, blank=True, help_text="Additional artist metadata")

    def __str__(self):
        return f"Artist Profile: {self.user.username}"

class Commission(BaseModel):
    """
    Represents a commission request for custom artwork.
    """
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    title = models.CharField(max_length=255, help_text="Title of the commission")
    description = models.TextField(help_text="Details of the commission requirements")
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Budget for the commission")
    requested_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="commissions_requested",
        help_text="User requesting the commission"
    )
    assigned_to = models.ForeignKey(
        ArtistProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissions_assigned",
        help_text="Artist assigned to the commission"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="requested", help_text="Current status of the commission")
    # Placeholder for payment or contract integration
    contract_url = models.URLField(null=True, blank=True, help_text="URL for the commission contract or payment agreement")

    def __str__(self):
        return self.title

class MarketplaceListing(BaseModel):
    """
    Represents a marketplace listing for artworks available for sale or commission.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('removed', 'Removed'),
    ]
    title = models.CharField(max_length=255, help_text="Title of the listing")
    description = models.TextField(help_text="Description of the listing")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for the artwork")
    image = models.ImageField(upload_to="marketplace_listings/", help_text="Image for the listing")
    artist_profile = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,
        related_name="marketplace_listings",
        help_text="Artist profile associated with this listing"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", help_text="Listing status")
    # Placeholder for future payment system integration
    payment_details = models.JSONField(null=True, blank=True, help_text="Payment details or integration data")

    def __str__(self):
        return self.title

```


---
## apps\kreative\marketplace\serializers.py

```py
from rest_framework import serializers
from kreative.marketplace.models import ArtistProfile, Commission, MarketplaceListing

class ArtistProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ArtistProfile
        fields = [
            'id',
            'user',
            'biography',
            'portfolio_url',
            'metadata',
            'created_at',
            'updated_at'
        ]

class CommissionSerializer(serializers.ModelSerializer):
    requested_by = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Commission
        fields = [
            'id',
            'title',
            'description',
            'budget',
            'requested_by',
            'assigned_to',
            'status',
            'contract_url',
            'created_at',
            'updated_at'
        ]

class MarketplaceListingSerializer(serializers.ModelSerializer):
    artist_profile = ArtistProfileSerializer(read_only=True)

    class Meta:
        model = MarketplaceListing
        fields = [
            'id',
            'title',
            'description',
            'price',
            'image',
            'artist_profile',
            'status',
            'payment_details',
            'created_at',
            'updated_at'
        ]

```


---
## apps\kreative\marketplace\views.py

```py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from kreative.marketplace.models import ArtistProfile, Commission, MarketplaceListing
from kreative.marketplace.serializers import (
    ArtistProfileSerializer,
    CommissionSerializer,
    MarketplaceListingSerializer
)

class ArtistProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les profils d'artistes.
    Permet aux artistes de gérer leur profil et leur portfolio.
    """
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que le profil de l'artiste connecté
        return ArtistProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement le profil à l'utilisateur
        serializer.save(user=self.request.user)


class CommissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commissions artistiques.
    Permet de créer, mettre à jour et suivre les demandes de commissions.
    """
    serializer_class = CommissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les commissions créées par l'utilisateur
        return Commission.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement la commission à l'utilisateur
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """
        Action personnalisée pour mettre à jour le statut d'une commission.
        """
        commission = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {"error": "Le champ 'status' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        commission.status = new_status
        commission.save()
        return Response(self.get_serializer(commission).data)


class MarketplaceListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les annonces du marketplace.
    Permet de créer, mettre à jour et supprimer des annonces d'œuvres ou de commissions.
    """
    serializer_class = MarketplaceListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les annonces créées par l'utilisateur
        return MarketplaceListing.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement l'annonce à l'utilisateur
        serializer.save(created_by=self.request.user)

```


---
## apps\kreative\marketplace\urls.py

```py
# apps/kreative/marketplace/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kreative.marketplace.views import (
    ArtistProfileViewSet,
    CommissionViewSet,
    MarketplaceListingViewSet,
)

app_name = "marketplace"

router = DefaultRouter()
router.register(r"artist_profiles",       ArtistProfileViewSet)
router.register(r"commissions",           CommissionViewSet)
router.register(r"marketplace_listings",  MarketplaceListingViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]

```


---
## apps\kreative\marketplace\migrations\0001_initial.py

```py
# Generated by Django 5.1.6 on 2025-02-11 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtistProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "biography",
                    models.TextField(
                        blank=True, help_text="Artist biography", null=True
                    ),
                ),
                (
                    "portfolio_url",
                    models.URLField(
                        blank=True, help_text="URL to the artist's portfolio", null=True
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True, help_text="Additional artist metadata", null=True
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        help_text="Associated user for the artist profile",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="artist_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Commission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(
                        help_text="Title of the commission", max_length=255
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Details of the commission requirements"
                    ),
                ),
                (
                    "budget",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="Budget for the commission",
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("requested", "Requested"),
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="requested",
                        help_text="Current status of the commission",
                        max_length=20,
                    ),
                ),
                (
                    "contract_url",
                    models.URLField(
                        blank=True,
                        help_text="URL for the commission contract or payment agreement",
                        null=True,
                    ),
                ),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        help_text="Artist assigned to the commission",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="commissions_assigned",
                        to="marketplace.artistprofile",
                    ),
                ),
                (
                    "requested_by",
                    models.ForeignKey(
                        help_text="User requesting the commission",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="commissions_requested",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MarketplaceListing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "title",
                    models.CharField(help_text="Title of the listing", max_length=255),
                ),
                (
                    "description",
                    models.TextField(help_text="Description of the listing"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Price for the artwork",
                        max_digits=10,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Image for the listing",
                        upload_to="marketplace_listings/",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("sold", "Sold"),
                            ("removed", "Removed"),
                        ],
                        default="active",
                        help_text="Listing status",
                        max_length=20,
                    ),
                ),
                (
                    "payment_details",
                    models.JSONField(
                        blank=True,
                        help_text="Payment details or integration data",
                        null=True,
                    ),
                ),
                (
                    "artist_profile",
                    models.ForeignKey(
                        help_text="Artist profile associated with this listing",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="marketplace_listings",
                        to="marketplace.artistprofile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

```


---
## apps\kreative\marketplace\forms.py

```py

```
