"""This module contains configuration for use during development."""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_AGE_REMEMBER = 1209600
CHANGE_EMAIL_EXPIRY_MINUTES_TIME = 5
INACTIVE_EMAIL_EXPIRY_MINUTES_TIME = 2
