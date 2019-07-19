from .common import *
import dj_database_url 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#email backend and vars
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = "sgbackend.SendgridBackend"
# EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = "support@ImageQ"
# SENDGRID_API_KEY = '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'
# SENDGRID_SANDBOX_MODE_IN_DEBUG = False
# SENDGRID_ECHO_TO_STDOUT = True

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://rltwwwpyvwzzlt:e3165ba253100fcb66c589901607b44bd8d81404ea400191333c85bbec952a63@ec2-54-75-230-41.eu-west-1.compute.amazonaws.com:5432/d31k5vbdupfdvg") # environment key provided by heroku

#heroku database
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

PREDICTION_API = "http://172.104.78.30/predict"

# cloudinary media storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'