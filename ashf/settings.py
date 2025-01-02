from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
GEOIP_PATH = BASE_DIR/'geoip'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n+h-#lmf1wghd9)=07+ns@ot65h47)z**0qg%o^0m248(v0e+8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

RECAPTCHA_PUBLIC_KEY = '6LeKz2oqAAAAAJ7sfTw9FG4q0bc0PENdGLzqmZJ5'
RECAPTCHA_PRIVATE_KEY = '6LeKz2oqAAAAAJOE7H5ReD01e5IU2U9PLS_Ce_YE'

# Optional: Specify the version of reCAPTCHA you want to use
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True
# Application definition

INSTALLED_APPS = [
    # "admin_interface",
    # "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'aashfApp',
    'aashfApp.apps.AashfappConfig',
    'ahospital',
    'django_recaptcha',
    'ckeditor',
]

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        # additional configuration here
    },
}
# X_FRAME_OPTIONS = "SAMEORIGIN"
# SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ashf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
             #   'aashfApp.context_processors.my_custom_context',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ashf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CACHE_TTL = 60 * 1500

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#         "KEY_PREFIX": "example"
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "ahospital.MyUser"
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = '/home/ashfoundation/public_html/media/'
STATICFILES_DIRS = [
    BASE_DIR/'static',
]
# STATIC_ROOT = '/home/ashfoundation/public_html/static/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/hospital/login/'
LOGIN_REDIRECT_URL = '/hospital'
LOGOUT_REDIRECT_URL  = '/hospital'

#Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'mail.ashfoundation.ngo'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'info@ashfoundation.ngo'
EMAIL_HOST_PASSWORD = 'Ashfoundation123'
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
PASSWORD_RESET_TIMEOUT = 900


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = 'mail.ashfoundation.ngo'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'info@ashfoundation.ngo'
# EMAIL_HOST_PASSWORD = 'Ashfoundation123'
# EMAIL_USE_TLS = True

# PASSWORD_RESET_TIMEOUT = 900