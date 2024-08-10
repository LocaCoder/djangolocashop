import os
from pathlib import Path
from django.contrib.messages import constants as messages


DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    }
}


# Send Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'amir1386abbas4838@gmail.com'
EMAIL_HOST_PASSWORD = 'nbqy nbzw nvdu gztp'
EMAIL_USE_TLS = True


