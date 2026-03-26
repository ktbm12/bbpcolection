from .base import *  # 🔥 OBLIGATOIRE

import os
import ssl
from pathlib import Path
import environ
import dj_database_url

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "bbpproject"
env = environ.Env()

env_file = BASE_DIR / ".env"
if env_file.exists():
    env.read_env(str(env_file))

# -------------------------
# DEBUG et ALLOWED_HOSTS
# -------------------------
DEBUG = env.bool("DEBUG", False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# -------------------------
# DATABASES (Render PostgreSQL)
# -------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# -------------------------
# STATIC & MEDIA
# -------------------------
STATIC_ROOT = str(BASE_DIR / "staticfiles")
MEDIA_ROOT = str(APPS_DIR / "media")

# -------------------------
# PORT (Render)
# -------------------------
PORT = int(os.environ.get("PORT", 10000))

# -------------------------
# REDIS & CELERY
# -------------------------
REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None
CELERY_REDIS_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL