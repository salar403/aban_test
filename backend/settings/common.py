import os
from pathlib import Path

from backend.environments import (
    PLATFORM,
    BACKEND_POSTGRES_HOST,
    BACKEND_POSTGRES_NAME,
    BACKEND_POSTGRES_PASSWORD,
    BACKEND_POSTGRES_PORT,
    BACKEND_POSTGRES_USERNAME,
    BACKEND_REDIS_HOST,
    BACKEND_REDIS_PORT,
    REDIS_CACHE_LOCK,
    REDIS_CELERY_BACKEND,
    REDIS_CELERY_BROKER,
    REDIS_COIN_INFO,
    REDIS_DEFAULT,
    REDIS_KEYS,
    REDIS_MANAGEMENT,
    REDIS_OTP,
    REDIS_PASSWORD_TRY,
    REDIS_RATELIMIT,
    REDIS_TOKENS,
    REDIS_CHANNEL_LAYER,
    SWAGGER_URL,
)


DEBUG = bool(PLATFORM != "production")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-k4im^mpm#!cc4c9ldmu@$(b+fe84$)h^l8s@i$3mkjt0g%1cmq"

CORS_ALLOWED_ORIGINS = [
    "https://api.abandev.ir",
    "https://abandev.ir",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

INSTALLED_APPS = [
    "user",
    "exchange",
    "accounting",
    "report",
    "trade",
    "rest_framework",
    "drf_yasg",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "backend.middlewares.ratelimit.RateLimitingMiddleware",
    "backend.middlewares.authorization.CustomAuthorization",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "backend.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": BACKEND_POSTGRES_NAME,
        "USER": BACKEND_POSTGRES_USERNAME,
        "PASSWORD": BACKEND_POSTGRES_PASSWORD,
        "HOST": BACKEND_POSTGRES_HOST,
        "PORT": BACKEND_POSTGRES_PORT,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_DEFAULT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "otp": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_OTP}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "management": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_MANAGEMENT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "ratelimit": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_RATELIMIT}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "tokens": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_TOKENS}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "keys": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_KEYS}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "passrate": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_PASSWORD_TRY}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "coin_info": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_COIN_INFO}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "cache_lock": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_CACHE_LOCK}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_CHANNEL_LAYER}"
            ],
        },
    },
}

CELERY_BROKER_URL = (
    f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_CELERY_BROKER}"
)
CELERY_RESULT_BACKEND = (
    f"redis://{BACKEND_REDIS_HOST}:{BACKEND_REDIS_PORT}/{REDIS_CELERY_BACKEND}"
)
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 31540000}
CELERY_CREATE_MISSING_QUEUES = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
    },
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
    "DEFAULT_API_URL": SWAGGER_URL,
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

USE_I18N = True
USE_L10N = True
TIME_ZONE = "Asia/Tehran"
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

OTP_EXPIRE_TIME = 60
OTP_CODE_MAX_TRY = 3
OTP_DIGIT_COUNT = 6
OTP_IP_RATE_LIMIT = 30

REQUEST_RATE_1MIN = 100
REQUEST_RATE_15MIN = 500
REQUEST_RATE_1HOUR = 1000
REQUEST_BLOCK_RATE = 100
BAD_REQUEST_LEVERAGE = 1
UNUSUAL_REQUEST_RATE = 120
REQUEST_TIME_DRIFT = 10

USER_TOKEN_TIMEVALID = 8 * 60 * 60.0
TOKEN_KEY_TIMEVALID = 8 * 60 * 60.0

WEBSOCKET_DEADTIME = 30 * 60

PASSWORD_HASH_MAX_MEMORY = 10 * 1024
PASSWORD_HASH_MAX_THREADS = 1
PASSWORD_HASH_MAX_TIME = 1
PASSWORD_HASH_SALT_LEN = 32
PASSWORD_HASH_LEN = 256

AUTH_TOKEN_HEADER = "Authorization"
AUTH_TOKEN_PERFIX = "Bearer"
