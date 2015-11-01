import logging
from settings import *

logging.disable(logging.INFO)
logging.disable(logging.WARNING)

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':':memory:',
    }
}
