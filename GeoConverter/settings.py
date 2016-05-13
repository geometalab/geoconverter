"""
Django settings for osmaxx project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import environ
import os
from GeoConverter import get_metadata

ROOT_DIR = environ.Env().path(
    'APP_DIR', default=str(
        environ.Path(
            os.path.dirname(__file__)) - 1))
APPS_DIR = ROOT_DIR.path('OGRgeoConverter')

DATA_DIR = environ.Env().path('DATA_DIR', default='/data')
OUTPUT_DIR = environ.Env().path('OUTPUT_DIR', default='/output')
STATICFILES_DIR = environ.Env().path('STATICFILES_DIR', default='/staticfiles')

METADATA = get_metadata()

env = environ.Env(
    DJANGO_ADMINS=(str, 'Some User;user@example.org'),
    DJANGO_ALLOWED_HOSTS=(str, 'localhost,127.0.0.1,0.0.0.0'),
    DJANGO_CACHE_DEFAULT_URL=(environ.Env.cache_url, 'locmemcache://'),
    DJANGO_DB_CONVERTER_URL=(environ.Env.db_url, 'sqlite:///' +
                             str(DATA_DIR('ogrgeoconverter.sqlite'))),
    DJANGO_DB_DEFAULT_URL=(environ.Env.db_url, 'sqlite:///' +
                           str(DATA_DIR('default.sqlite'))),
    DJANGO_DB_JOBS_URL=(environ.Env.db_url, 'sqlite:///' +
                        str(DATA_DIR('conversionjobs.sqlite'))),
    DJANGO_DB_LOGS_URL=(environ.Env.db_url, 'sqlite:///' +
                        str(DATA_DIR('log.sqlite'))),
    DJANGO_DB_SESSIONS_URL=(environ.Env.db_url, 'sqlite:///' +
                            str(DATA_DIR('sessions.sqlite'))),
    DJANGO_DEBUG=(bool, False),
    DJANGO_DEFAULT_FROM_EMAIL=(str, 'webmaster@localhost'),
    DJANGO_EMAIL_BACKEND=(str,
                          'django.core.mail.backends.filebased.EmailBackend'),
    DJANGO_EMAIL_FILE_PATH=(str, str(DATA_DIR('emails'))),
    DJANGO_EMAIL_HOST=(str, 'localhost'),
    DJANGO_EMAIL_HOST_PASSWORD=(str, ''),
    DJANGO_EMAIL_HOST_USER=(str, ''),
    DJANGO_EMAIL_PORT=(int, 25),
    DJANGO_EMAIL_SUBJECT_PREFIX=(str, '[GeoConverter] '),
    DJANGO_EMAIL_TIMEOUT=(int, 25),
    DJANGO_EMAIL_USE_SSL=(bool, False),
    DJANGO_EMAIL_USE_TLS=(bool, False),
    DJANGO_ENV_FILE=(str, str(ROOT_DIR('.env'))),
    DJANGO_MEDIA_ROOT=(str, str(ROOT_DIR)),
    DJANGO_PRIVATE_MEDIA_ROOT=(str, str(ROOT_DIR)),
    DJANGO_SECRET_KEY=(str, 'DummyKeyToBeChanged'),
    DJANGO_SERVER_EMAIL=(str, 'root@localhost'),
    DJANGO_STATICFILES_DIRS=(list, [str(ROOT_DIR('static'))]),
    DJANGO_STATICFILES_STORAGE=(str,
                                'django.contrib.staticfiles.storage.StaticFilesStorage'),
    DJANGO_STATIC_ROOT=(str, str(STATICFILES_DIR)),
    DJANGO_STATIC_URL=(str, '/static/'),
    DJANGO_THIRD_PARTY_APPS=(str, ''),
    DJANGO_X_FRAME_OPTIONS=(str, 'SAMEORIGIN'),)

environ.Env.read_env(env('DJANGO_ENV_FILE'))  # reading potential .env file


def tolist_with_env_lookup(x):
    return [x for x in filter(None, [y for y in x.split(',') if not y.startswith(
        '$')] + [env(y[1:], default=None) for y in x.split(',') if y.startswith('$')])]

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
]

THIRD_PARTY_APPS = []
THIRD_PARTY_APPS += env(
    'DJANGO_THIRD_PARTY_APPS',
    cast=list,
    parse_default=True)

# Apps specific for this project go here.
LOCAL_APPS = [
    'OGRgeoConverter',
    # 'version',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    # 'sites': 'geoconverter.contrib.sites.migrations',
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env("DJANGO_DEBUG")

# See: https://docs.djangoproject.com/en/1.8/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = [
    str(APPS_DIR('fixtures')),
]

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND")
EMAIL_HOST = env("DJANGO_EMAIL_HOST")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER")
EMAIL_PORT = env("DJANGO_EMAIL_PORT")
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX")
EMAIL_TIMEOUT = env("DJANGO_EMAIL_TIMEOUT")
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL")
EMAIL_USE_TLS = env('DJANGO_EMAIL_USE_TLS')
EMAIL_USE_SSL = env('DJANGO_EMAIL_USE_SSL')

EMAIL_FILE_PATH = str(env("DJANGO_EMAIL_FILE_PATH"))
# allow default setting (unset) if the variable isn't set in the environment
if not EMAIL_FILE_PATH:
    del EMAIL_FILE_PATH
else:
    if not os.path.isdir(EMAIL_FILE_PATH):
        os.makedirs(EMAIL_FILE_PATH)

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = env(
    'DJANGO_ADMINS',
    cast=[
        lambda x: tuple(
            x.split(';'))],
    parse_default=True)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# What database is used is determined by a database router (see
# DATABASE_ROUTERS below)
DATABASES = {
    'default': env.db("DJANGO_DB_DEFAULT_URL"),
    'sessions_db': env.db("DJANGO_DB_SESSIONS_URL"),
    'ogrgeoconverter_db': env.db("DJANGO_DB_CONVERTER_URL"),
    'ogrgeoconverter_log_db': env.db("DJANGO_DB_LOGS_URL"),
    'ogrgeoconverter_conversion_jobs_db': env.db("DJANGO_DB_JOBS_URL"),
}

DATABASE_ROUTERS = ['GeoConverter.database.DatabaseRouter']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Zurich'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/#the-templates-settings
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [
#             str(APPS_DIR.path('templates')),
#         ],
#         'OPTIONS': {
#             'context_processors': [
# #                 'django.contrib.auth.context_processors.auth',
# #                 'django.template.context_processors.debug',
# #                 'django.template.context_processors.i18n',
# #                 'django.template.context_processors.media',
# #                 'django.template.context_processors.static',
# #                 'django.template.context_processors.tz',
# #                 'django.contrib.messages.context_processors.messages',
# #                 'django.core.context_processors.request',
#             ],
#             'loaders': [
#                 'django.template.loaders.filesystem.Loader',
#                 'django.template.loaders.app_directories.Loader',
#             ]
#         },
#     },
# ]
TEMPLATE_DIRS = (
    str(ROOT_DIR.path('templates')),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = env('DJANGO_STATIC_ROOT')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = env('DJANGO_STATIC_URL')

# See:
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = env.list('DJANGO_STATICFILES_DIRS')

# See:
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = env('DJANGO_STATICFILES_STORAGE')

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root

# data & media

MEDIA_ROOT = env("DJANGO_MEDIA_ROOT")
PRIVATE_MEDIA_ROOT = env("DJANGO_PRIVATE_MEDIA_ROOT")

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = ''

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'GeoConverter.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'GeoConverter.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

CACHES = {
    'default': env.cache('DJANGO_CACHE_DEFAULT_URL'),
}

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
}

# Security - defaults taken from Django 1.8 (not secure enough for production)
SECRET_KEY = env("DJANGO_SECRET_KEY")
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env(
    'DJANGO_ALLOWED_HOSTS',
    cast=tolist_with_env_lookup,
    parse_default=True)

X_FRAME_OPTIONS = env("DJANGO_X_FRAME_OPTIONS")

# Session ends when user closes his browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
