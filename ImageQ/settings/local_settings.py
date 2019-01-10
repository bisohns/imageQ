from .common import *

#email backend and vars
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = "support@ImageQ"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'imageqdb',
        'USER': 'imageq',
        'PASSWORD': 'imageq',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

