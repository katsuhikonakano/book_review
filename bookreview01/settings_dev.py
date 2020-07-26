from .settings import *

DEBUG = True

SECRET_KEY = 'gml-x%f_36ibid$2=t!uh0ra_(&8+v%#6#&r81%((w^a*gq*m#'

ALLOWED_HOSTS = []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'bookapp': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'users': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

