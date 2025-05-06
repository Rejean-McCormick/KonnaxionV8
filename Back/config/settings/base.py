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
