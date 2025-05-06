"""
common/constants.py

This module centralizes all global constants, default values, and shared strings for the Konnaxion platform.
It is intended to be imported wherever these common values are needed, ensuring consistency and reducing duplication.
"""

# -----------------------------------------------------------------------------
# Versioning
# -----------------------------------------------------------------------------
VERSION = "1.0.0"

# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------
API_BASE_PATH = "/api/v1/"

# -----------------------------------------------------------------------------
# Common Field Lengths
# -----------------------------------------------------------------------------
MAX_CHARFIELD_LENGTH = 255

# -----------------------------------------------------------------------------
# Status Constants
# -----------------------------------------------------------------------------
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"

# -----------------------------------------------------------------------------
# Date & Time Formats
# -----------------------------------------------------------------------------
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

# -----------------------------------------------------------------------------
# Error Messages
# -----------------------------------------------------------------------------
ERROR_NOT_FOUND = "The requested resource was not found."
ERROR_PERMISSION_DENIED = "You do not have permission to perform this action."
ERROR_INVALID_REQUEST = "Invalid request. Please check your input."

# -----------------------------------------------------------------------------
# Logging Levels
# -----------------------------------------------------------------------------
LOGGING_LEVEL_DEBUG = "DEBUG"
LOGGING_LEVEL_INFO = "INFO"
LOGGING_LEVEL_WARNING = "WARNING"
LOGGING_LEVEL_ERROR = "ERROR"
LOGGING_LEVEL_CRITICAL = "CRITICAL"

# -----------------------------------------------------------------------------
# Celery & Asynchronous Task Constants
# -----------------------------------------------------------------------------
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# -----------------------------------------------------------------------------
# Pagination & Related Defaults
# -----------------------------------------------------------------------------
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# -----------------------------------------------------------------------------
# OAuth & JWT Settings
# -----------------------------------------------------------------------------
JWT_ALGORITHM = "HS256"
# JWT expiration in seconds (e.g., 1 hour)
JWT_EXPIRATION_DELTA = 3600  

# -----------------------------------------------------------------------------
# Authentication Settings
# -----------------------------------------------------------------------------
# Reference to the custom user model defined in the konnaxion_core app
AUTH_USER_MODEL = "konnaxion.konnaxion_core.CustomUser"

# -----------------------------------------------------------------------------
# Event-Driven & Signal Naming
# -----------------------------------------------------------------------------
SIGNAL_USER_UPDATED = "user_updated"
SIGNAL_REPUTATION_CHANGED = "reputation_changed"

# -----------------------------------------------------------------------------
# WebSocket Channel Names (for Django Channels or similar)
# -----------------------------------------------------------------------------
CHANNEL_NOTIFICATIONS = "notifications_channel"
CHANNEL_CHAT = "chat_room"

# -----------------------------------------------------------------------------
# Environment Variable Keys
# -----------------------------------------------------------------------------
# These keys should match what is set in your .env files or environment configuration.
ENV_SECRET_KEY = "SECRET_KEY"
ENV_DEBUG = "DEBUG"
ENV_ALLOWED_HOSTS = "ALLOWED_HOSTS"
ENV_DATABASE_URL = "DATABASE_URL"
ENV_CELERY_BROKER_URL = "CELERY_BROKER_URL"
ENV_CELERY_RESULT_BACKEND = "CELERY_RESULT_BACKEND"
ENV_OAUTH_CLIENT_ID = "OAUTH_CLIENT_ID"
ENV_OAUTH_CLIENT_SECRET = "OAUTH_CLIENT_SECRET"
ENV_JWT_SECRET_KEY = "JWT_SECRET_KEY"
ENV_SENTRY_DSN = "SENTRY_DSN"

# -----------------------------------------------------------------------------
# Frontend and Path Variables (Reference for settings.py or manage.py)
# -----------------------------------------------------------------------------
# These paths are typically defined in your settings or management files,
# but are included here for reference.
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, "apps")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
ENV_DIR = os.path.join(BASE_DIR, ".envs")
VENV_DIR = os.path.join(BASE_DIR, ".venv")
