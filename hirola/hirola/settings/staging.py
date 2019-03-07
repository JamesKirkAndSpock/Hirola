"""
This module contains setting configurations for use in the
production stage.
"""
import os

DEBUG = False
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
MEDIA_URL = os.environ.get('GS_BUCKET_URL')
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATIC_ROOT = '/var/www/html/static/'
SESSION_COOKIE_AGE = int(os.environ.get('SESSION_COOKIE_AGE'), base=0)
SESSION_COOKIE_AGE_REMEMBER = int(
    os.environ.get('SESSION_COOKIE_AGE_KNOWN_DEVICE'), base=0
    )
CHANGE_EMAIL_EXPIRY_MINUTES_TIME = int(os.environ.get(
    'CHANGE_EMAIL_EXPIRY_MINUTES_TIME'), base=0)
INACTIVE_EMAIL_EXPIRY_MINUTES_TIME = int(
    os.environ.get('INACTIVE_EMAIL_EXPIRY_MINUTES_TIME'), base=0
    )
