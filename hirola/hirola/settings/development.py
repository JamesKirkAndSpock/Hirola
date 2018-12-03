from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_AGE_REMEMBER = 1209600
