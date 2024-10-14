"""
Django settings for lockey project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fv(!qi4xn=nd^$=o3!07yk=b!vwn@r)v^2i2y$cp8ugy8xhx_-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Application definition

INSTALLED_APPS = [
    'django_extensions',  # extra admin commands (devenv)
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django_filters',
    'rest_framework',
    'drf_standardized_errors',
    'corsheaders',
    'knox',
    'apps.whitelist',
    'apps.permission',
    'apps.group',
    'apps.user',
    'apps.folder',
    'apps.credential',
]

AUTH_USER_MODEL = 'user.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'middleware.security.AuthenticationMiddleware',
    'middleware.security.AuditLogMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.security.AccessWhitelistMiddleware',
]

ROOT_URLCONF = 'lockey.urls'


WSGI_APPLICATION = 'lockey.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'sqlite3.db',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'validator.password_validators.ComplexityValidator',
    },
    {
        'NAME': 'validator.password_validators.ReusedValidator',
    },
    {
        'NAME': 'validator.password_validators.MinimumChangeIntervalValidator',
    },
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'utils.pagination.Pagination',
    # 'PAGE_SIZE': os.getenv('DJANGO_PAGE_SIZE', 5),
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
}

DRF_STANDARDIZED_ERRORS = {"ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True}

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': timedelta(hours=10),
    'USER_SERIALIZER': 'apps.user.api.serializers.UserGetSerializer',
    'TOKEN_LIMIT_PER_USER': 10,
    'AUTO_REFRESH': True,
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'utils.logging.ColoredFormatter',
            'format': '%(asctime)s.%(msecs)03d %(levelname)-8s [%(process)d-%(thread)d] [%(name)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': os.getenv('ORM_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'lockey': {
            'handlers': ['console'],
            'level': os.getenv('LOCKEY_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        'lockey.security': {
            'handlers': ['console'],
            'level': os.getenv('LOCKEY_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
APPEND_SLASH = False

DEFAULT_MAX_DIGIT = 34
DEFAULT_DECIMAL_PLACES = 2
