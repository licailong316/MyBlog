from .base import *  # noqa: F401

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'landblog',
        'HOST': '127.0.0.1',
        'USER': 'licailong',
        'PASSWORD': '316licailongLCL@',
        'PORT': 3306,
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
