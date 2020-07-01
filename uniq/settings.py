import os

from cloghandler import ConcurrentRotatingFileHandler
from configurations import Configuration
from dotenv import load_dotenv
import datetime
from django.utils.translation import ngettext


load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'uniq')


class BaseConfiguration(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = os.getenv('SECRET_KEY')

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    INSTALLED_APPS = [
        'modeltranslation',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.postgres',
        'django_celery_beat',
        'django_celery_results',
        'rest_framework',
        'corsheaders',
        'core',
        'utils',
        'auth_',
        'tests'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.locale.LocaleMiddleware'
    ]

    ROOT_URLCONF = 'uniq.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(PROJECT_DIR, 'templates'), ],
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

    WSGI_APPLICATION = 'uniq.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'uniq',
            'USER': 'admin',
            'PASSWORD': '1234',
            'HOST': "localhost",
            'PORT': '5432'
        }
    }

    AUTH_USER_MODEL = "auth_.MainUser"

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

    WAITING_TIME_ATTEMPTS_MIN = 3
    gettext = lambda s: s
    LANGUAGES = (
        ('en', gettext('English')),
        ('ru', gettext('Russian')),
    )

    LANGUAGE_CODE = 'ru'
    MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
    MODELTRANSLATION_LANGUAGES = ('en', 'ru')
    MODELTRANSLATION_TRANSLATION_REGISTRY = 'uniq.translation'

    LOCALE_PATHS = (
        os.path.join(PROJECT_DIR, '../locale'),
    )
    TIME_ZONE = 'Asia/Almaty'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'
    STATIC_ROOT = "/static"
    STATICFILES_DIRS = (os.path.join(PROJECT_DIR, "static"),)

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    SITE_URL = 'http://localhost:8000'

    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    FROM_EMAIL = os.getenv('FROM_EMAIL')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = True

    LIMIT = 10

    ADMINS = (
    )
    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
        'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
    }
    JWT_AUTH = {
        'JWT_EXPIRATION_DELTA': datetime.timedelta(days=300),
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    }
    CORS_ORIGIN_ALLOW_ALL = True

    CELERY_BROKER_URL = 'pyamqp://{user}:{pwd}@{host}:{port}/{vhost}'.format(
        user=os.getenv('RABBIT_USER', 'guest'),
        pwd=os.getenv('RABBIT_PASSWORD', 'guest'),
        host=os.getenv('RABBIT_HOST', 'rabbit1'),
        port=os.getenv('RABBIT_PORT', '5672'),
        vhost=os.getenv('RABBIT_VHOST', '/'))
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
    CELERY_RESULT_BACKEND = 'django-db'

    # Sensible settings for celery
    CELERY_ALWAYS_EAGER = False
    CELERY_ACKS_LATE = True
    CELERY_TASK_PUBLISH_RETRY = True
    CELERY_DISABLE_RATE_LIMITS = False

    # By default we will ignore result
    # If you want to see results and try out tasks interactively, change it to False
    # Or change this setting on tasks level
    CELERY_IGNORE_RESULT = True
    CELERY_SEND_TASK_ERROR_EMAILS = False
    CELERY_TASK_RESULT_EXPIRES = 600

    FILE_UPLOAD_PERMISSIONS = 0o644
    #
    # LOGS_BASE_DIR = os.getenv('LOGS_BASE_DIR', 'logs')
    #
    # LOGGING = {
    #     'version': 1,
    #     'disable_existing_loggers': False,
    #     'formatters': {
    #         'verbose': {
    #             'format': '[%(levelname)s] %(asctime)s path: %(pathname)s module: %(module)s method: %(funcName)s  row: %(lineno)d message: %(message)s'
    #         },
    #     },
    #     'handlers': {
    #         'default': {
    #             'level': 'INFO',
    #             'class': 'logging.handlers.ConcurrentRotatingFileHandler',
    #             'filename': os.path.join(LOGS_BASE_DIR, 'info.log'),
    #             'maxBytes': 1024 * 1024 * 20,  # 20 MB
    #             'backupCount': 30,
    #             'formatter': 'verbose',
    #         },
    #         'error': {
    #             'level': 'ERROR',
    #             'class': 'logging.handlers.TimedRotatingFileHandler',
    #             'formatter': 'verbose',
    #             'filename': os.path.join(LOGS_BASE_DIR, 'error.log'),
    #             'when': 'midnight',
    #             'backupCount': 30,
    #         },
    #     },
    #     'loggers': {
    #         '': {
    #             'handlers': ['default', 'error'],
    #             'level': 'INFO',
    #             'propagate': True
    #         },
    #     }
    # }
    #
    # SUIT_CONFIG = {
    #     'ADMIN_NAME': 'uniq'
    # }


class Dev(BaseConfiguration):
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    SITE_URL = ''
    STATIC_ROOT = '/uniq/static'
    MEDIA_ROOT = '/uniq/media'


class Prod(BaseConfiguration):
    DEBUG = False
    ALLOWED_HOSTS = ['']
    SITE_URL = ''
    CELERY_SEND_TASK_ERROR_EMAILS = False
    STATIC_ROOT = '/uniq/static'
    MEDIA_ROOT = '/uniq/media'
