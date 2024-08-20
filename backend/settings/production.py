import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from backend.environments import SENTRY_DSN_ADDRESS

sentry_sdk.init(dsn=SENTRY_DSN_ADDRESS, integrations=[DjangoIntegration()])

ALLOWED_HOSTS = ["api.abandev.ir"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False
