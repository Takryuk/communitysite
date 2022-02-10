import environ

from .base import *


env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = env('DEV_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'communitysite-db',
        'USER': 'communitysite_user',
        'PASSWORD': 'ta.ad.20317',  # ユーザー作った時のパスワード
        'HOST': 'localhost',
        'PORT': '',

    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
