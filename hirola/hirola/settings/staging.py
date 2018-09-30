from .base import *

DEBUG = False
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
MEDIA_URL = os.environ.get('GS_BUCKET_URL')
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATIC_ROOT = '/var/www/html/static/'