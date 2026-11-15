from pathlib import Path
import os
import sys
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=False)


def env_bool(name, default=False):
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_csv(name, default=""):
    raw = os.environ.get(name, default).replace(";", ",")
    return [item.strip() for item in raw.split(",") if item.strip()]


def public_origin(value):
    value = value.strip().rstrip("/")
    if not value:
        return "", ""
    if value.startswith(("http://", "https://")):
        return value, (urlparse(value).hostname or "")
    host = value.split("/")[0].split(":")[0]
    return f"https://{host}", host


SECRET_KEY = (
    os.environ.get("SECRET_KEY")
    or os.environ.get("DJANGO_SECRET_KEY")
    or os.environ.get("django_secret_key")
    or ""
).strip().strip("'\"")
DEBUG = env_bool("DEBUG", default=False)

if not SECRET_KEY:
    raise ImproperlyConfigured(
        "SECRET_KEY is missing. Set django_secret_key in .env for local work, "
        "or SECRET_KEY in the PaaS environment for production."
    )

ALLOWED_HOSTS = env_csv("ALLOWED_HOSTS", "*")
CSRF_TRUSTED_ORIGINS = [
    origin.rstrip("/")
    for origin in env_csv("CSRF_TRUSTED_ORIGINS")
    if origin.startswith(("http://", "https://"))
]
app_url = os.environ.get("APP_URL", "").strip().rstrip("/")
if app_url:
    origin, host = public_origin(app_url)
    if origin and origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)
    if host and host not in ALLOWED_HOSTS and "*" not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)
for host in ALLOWED_HOSTS:
    if host in {"*", ""} or host.startswith("."):
        continue
    origin = f"https://{host}"
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

SITE_URL = os.environ.get("SITE_URL", "").strip().rstrip("/")
if not SITE_URL and app_url:
    SITE_URL = app_url if app_url.startswith(("http://", "https://")) else f"https://{app_url}"
if SITE_URL.startswith(("http://", "https://")) and SITE_URL not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(SITE_URL)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 180
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
]

MIDDLEWARE = [
    'config.middleware.HealthCheckMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'products.context_processors.shop',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


DB_DIR = BASE_DIR / 'DB'


def sqlite_path():
    configured = os.environ.get("SQLITE_PATH", "").strip()
    path = Path(configured) if configured else DB_DIR / "db.sqlite3"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": sqlite_path(),
        "OPTIONS": {"timeout": 20},
    }
}


AUTH_PASSWORD_VALIDATORS = [
]

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
_media_root = Path(os.environ.get("MEDIA_ROOT", BASE_DIR / "media"))
if not _media_root.is_absolute():
    _media_root = BASE_DIR / _media_root
MEDIA_ROOT = _media_root
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': (
            'django.contrib.staticfiles.storage.StaticFilesStorage'
            if DEBUG
            else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        ),
    },
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": str(BASE_DIR / ".cache"),
        "TIMEOUT": 120,
        "OPTIONS": {"MAX_ENTRIES": 200},
    }
}
if "test" in sys.argv:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }


MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "plain"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}
