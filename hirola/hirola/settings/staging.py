from .base import *

DEBUG = False
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
MEDIA_URL = os.environ.get('GS_BUCKET_URL')
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATIC_ROOT = '/var/www/html/static/'
# SESSION_COOKIE_AGE=int(os.environ.get('SESSION_COOKIE_AGE'), base=0)
# SESSION_COOKIE_AGE_REMEMBER=int(os.environ.get('SESSION_COOKIE_AGE_KNOWN_DEVICE'))
