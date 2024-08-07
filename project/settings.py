from pathlib import Path
import datetime
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*', 'https://*.momyez.up.railway.app/']

CORS_ALLOW_ALL_ORIGINS = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1rcgs+lmoj0ox!#g^5rf9--aw)i&7%i#wtf+nvt&pa(96i9f)&'


TIME_ZONE = 'Africa/Cairo'
USE_TZ = False

DEBUG = True


AUTH_USER_MODEL = 'users.User'


# Application definition

INSTALLED_APPS = [
    
    'daphne',
    'channels',  
    'celery',
    'django_celery_results',
    'django_celery_beat',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'settings',
    'users',
    'locations',
    'otp',
    'flights',
    'flightsInfo',
    'reservations',
    'chat',
    'payment'
]
SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = "project.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'anaMomayz',
        'USER': 'Hmos',
        'PASSWORD': 'B14C5EG3acFc341DD3211c61CcA2CCD1',
        'HOST': 'momayz-test.cnm888kcg969.eu-central-1.rds.amazonaws.com',
        'PORT': '5432',
    },
}

REDIS_URL = 'master.momayzredistest.3l17qh.euc1.cache.amazonaws.com:6379'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'master.momayzredistest.3l17qh.euc1.cache.amazonaws.com:6379')],
        },
    },
}



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'basketserviceteam@gmail.com'
EMAIL_HOST_PASSWORD = 'pvwwmvluuvsvjiwc'
EMAIL_PORT = 587


CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = "Africa/Cairo"
CELERY_ENABLE_UTC = False
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True 

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

USE_I18N = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_VERIFICATION = 'none'


HMAC_KEY = '8BFDAE7FAC451F0EDC10C4DE660F69E5'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
SIMPLE_JWT  = {
    'USER_ID_FIELD': 'username',
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
}

REST_AUTH = {
        'USER_DETAILS_SERIALIZER' : 'users.serializers.CustomUserDetailsSerializer',
        'REGISTER_SERIALIZER': 'users.serializers.UserRegisterSerializer',
        
        'USE_JWT': True,
        'JWT_AUTH_COOKIE': 'my-app-auth',
        'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token',
        'JWT_AUTH_HTTPONLY':False,
}

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]       