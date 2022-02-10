import environ

from .base import *

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DATABASES = {
    'default': env.db()
}

DATABASES['default']['ATOMIC_REQUESTS'] = True
AXES_PROXY_COUNT = 1

EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = env('SENDGRID_API_KEY')
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_LOCALTIME = True
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_SSL_CERTFILE = None
# EMAIL_SSL_KEYFILE = None
# EMAIL_TIMEOUT = None
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'hello@ocealena.com'

