from .base import *

DEBUG = False
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
MEDIA_URL = os.environ.get('GS_BUCKET_URL')
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATIC_ROOT = '/var/www/html/static/'
SESSION_COOKIE_AGE=os.environ.get('SESSION_COOKIE_AGE')
SESSION_COOKIE_AGE_REMEMBER=os.environ.get('SESSION_CCOKIE_KD')