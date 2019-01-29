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

#heroku database
DATABASES = {
    'default': dj_database_url.parse('postgres://xguujvquxmfkkg:7bc9370d3a554fdc096675e99aafb77a95e0bf1a2cde6e4c14e9e3019361171d@ec2-54-247-125-116.eu-west-1.compute.amazonaws.com:5432/d6iei61f1ie5lg')
}

PREDICTION_API = "https://imageqapi.appspot.com/predict"