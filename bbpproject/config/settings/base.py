import os
import ssl
from pathlib import Path
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "bbpproject"
env = environ.Env()

# Lire .env si existant
env_file = BASE_DIR / ".env"
if env_file.exists():
    env.read_env(str(env_file))

# -------------------------
# DEBUG et ALLOWED_HOSTS
# -------------------------
DEBUG = env.bool("DEBUG", False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])  # Render injecte ton domaine ici

# -------------------------
# DATABASES
# -------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True  # SSL/TLS pour Render PostgreSQL
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# -------------------------
# STATIC & MEDIA
# -------------------------
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"

# -------------------------
# GUNicorn PORT
# -------------------------
# Render fournit automatiquement $PORT dans Dockerfile
PORT = int(os.environ.get("PORT", 10000))

# -------------------------
# REDIS & Celery
# -------------------------
REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None
CELERY_REDIS_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TIME_LIMIT = 5*60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# -------------------------
# Email, Stripe, PayPal, Allauth
# -------------------------
SECRET_KEY = env("SECRET_KEY")
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY", default="")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default="")
PAYPAL_CLIENT_ID = env("PAYPAL_CLIENT_ID", default="")
PAYPAL_CLIENT_SECRET = env("PAYPAL_CLIENT_SECRET", default="")
PAYPAL_MODE = env("PAYPAL_MODE", default="sandbox")