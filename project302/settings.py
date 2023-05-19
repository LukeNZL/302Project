"""
Django settings for project302 project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
#text
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o(d^@)7cn9#fkxo+*axpyc75q7$k0t#v)b%riybp2(=mry-f=%'



# Application definition

INSTALLED_APPS = [
    'kiwinco.apps.KiwincoConfig',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'project302',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project302.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project302.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# SECURITY WARNING: don't run with debug turned on in production!
if 'PYTHONPATH' in os.environ:
    DEBUG = True
    ALLOWED_HOSTS = ['.ap-southeast-2.elasticbeanstalk.com']

else:
    DEBUG = True
    ALLOWED_HOSTS = []

if 'RDS_DB_NAME' in os.environ:

    DATABASES = {
            'default': {
                'ENGINE':'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT'],
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
AWS_STORAGE_BUCKET_NAME = 'kiwinco-app-bucket'
AWS_S3_REGION_NAME = 'ap-southeast-2'



AWS_S3_ACCESS_KEY_ID = 'AKIAVMXNK6O7YQCXGRGT'
AWS_S3_SECRET_ACCESS_KEY = '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'



AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
   'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
#AWS_DEFAULT_ACL = 'public-read'
AWS_DEFAULT_ACL = None
AWS_LOCATION = 'static'
STATICFILES_DIRS = [
   'static',
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#STATIC_ROOT = 'static'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STRIPE_PUBLIC_KEY = "pk_live_51N60CYJDzpA491w3K0OtJz8a6VZUkc5ZiRMXoQyWBhNKVJou1M3JGzeGOqBRnA2ZO5zf6vonSuNUVEkKDfbjdAQv006M615wDv"
STRIPE_SECRET_KEY = "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"
STRIPE_WEBHOOK_SECRET = "whsec_b01dcfb8b6de8822091be6376def7cc3de3ee6105b176cf2b734ecf7136605d6"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'