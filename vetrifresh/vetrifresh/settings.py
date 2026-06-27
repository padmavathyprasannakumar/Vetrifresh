"""
Django settings for vetrifresh project.
Render + PostgreSQL + Cloudinary + Brevo + Cashfree + timeout ready.
"""

from pathlib import Path
from datetime import timedelta
import os

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

try:
    import cloudinary
except ImportError:
    cloudinary = None


# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# HELPER FUNCTIONS
# =========================
def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in (
        "true",
        "1",
        "yes",
        "on",
    )


def env_list(name, default=None):
    value = os.getenv(name, "")
    if value:
        return [item.strip().rstrip("/") for item in value.split(",") if item.strip()]
    return default or []


def env_int(name, default):
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


# =========================
# SECURITY
# =========================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-local-dev-key-change-this-before-deployment",
)

DEBUG = env_bool("DEBUG", True)


# =========================
# ALLOWED HOSTS
# =========================
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ALLOWED_HOSTS += env_list("ALLOWED_HOSTS")
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))


# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    # Django default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",

    # Cloudinary media storage
    "cloudinary_storage",
    "cloudinary",

    # Custom app
    "core",
]


# =========================
# CUSTOM USER MODEL
# =========================
AUTH_USER_MODEL = "core.User"


# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",

    # Static files on Render
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================
# URL / WSGI
# =========================
ROOT_URLCONF = "vetrifresh.urls"

WSGI_APPLICATION = "vetrifresh.wsgi.application"


# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================
# DATABASE
# =========================
# Local: SQLite
# Render: PostgreSQL using DATABASE_URL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL and dj_database_url:
    DATABASES["default"] = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=not DEBUG,
    )

    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"]["connect_timeout"] = env_int(
        "DB_CONNECT_TIMEOUT",
        10,
    )


# =========================
# PASSWORD VALIDATION
# =========================
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


# =========================
# LANGUAGE / TIME
# =========================
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =========================
# STATIC FILES
# =========================
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

# Important: keep this for django-cloudinary-storage compatibility.
# Do not use STORAGES here while using django-cloudinary-storage 0.3.0.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =========================
# CLOUDINARY / MEDIA FILES
# =========================
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "").strip()
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "").strip()

USE_CLOUDINARY = bool(
    CLOUDINARY_CLOUD_NAME
    and CLOUDINARY_API_KEY
    and CLOUDINARY_API_SECRET
)

# Remove CLOUDINARY_URL at runtime so old/wrong Render values cannot override
# CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET.
if USE_CLOUDINARY:
    os.environ.pop("CLOUDINARY_URL", None)

    if cloudinary:
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True,
        )

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
    "API_KEY": CLOUDINARY_API_KEY,
    "API_SECRET": CLOUDINARY_API_SECRET,
    "SECURE": True,
}

MEDIA_URL = "/media/"

MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", BASE_DIR / "media"))

if USE_CLOUDINARY:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# With Cloudinary on Render, keep this False.
SERVE_MEDIA_FILES = env_bool("SERVE_MEDIA_FILES", False)


# =========================
# DEFAULT PRIMARY KEY
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================
# CORS SETTINGS
# =========================
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5174",
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

FRONTEND_URL = os.getenv("FRONTEND_URL", "").strip().rstrip("/")
if FRONTEND_URL:
    CORS_ALLOWED_ORIGINS.append(FRONTEND_URL)

CORS_ALLOWED_ORIGINS += env_list("CORS_ALLOWED_ORIGINS")
CORS_ALLOWED_ORIGINS = list(dict.fromkeys(CORS_ALLOWED_ORIGINS))

CORS_ALLOW_CREDENTIALS = True


# =========================
# CSRF TRUSTED ORIGINS
# =========================
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5174",
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

if FRONTEND_URL:
    CSRF_TRUSTED_ORIGINS.append(FRONTEND_URL)

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

CSRF_TRUSTED_ORIGINS += env_list("CSRF_TRUSTED_ORIGINS")
CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS))


# =========================
# DEPLOYMENT SECURITY SETTINGS
# =========================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = False

    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    # Keep False on Render unless HTTPS redirect is confirmed working.
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", False)

    SECURE_HSTS_SECONDS = env_int("SECURE_HSTS_SECONDS", 0)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
        "SECURE_HSTS_INCLUDE_SUBDOMAINS",
        False,
    )
    SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", False)


# =========================
# DJANGO REST FRAMEWORK
# =========================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),

    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": env_int("API_PAGE_SIZE", 12),
}


# =========================
# JWT SETTINGS
# =========================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env_int("JWT_ACCESS_TOKEN_MINUTES", 1440)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env_int("JWT_REFRESH_TOKEN_DAYS", 7)
    ),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}


# =========================
# TIMEOUT SETTINGS
# =========================
EMAIL_TIMEOUT = env_int("EMAIL_TIMEOUT", 30)

CASHFREE_REQUEST_TIMEOUT = env_int("CASHFREE_REQUEST_TIMEOUT", 30)

EXTERNAL_API_TIMEOUT = env_int("EXTERNAL_API_TIMEOUT", 30)

SESSION_COOKIE_AGE = env_int("SESSION_COOKIE_AGE", 60 * 60 * 24 * 7)

PASSWORD_RESET_TIMEOUT = env_int("PASSWORD_RESET_TIMEOUT", 60 * 60)


# =========================
# FILE UPLOAD SETTINGS
# =========================
FILE_UPLOAD_MAX_MEMORY_SIZE = env_int(
    "FILE_UPLOAD_MAX_MEMORY_SIZE",
    10 * 1024 * 1024,
)

DATA_UPLOAD_MAX_MEMORY_SIZE = env_int(
    "DATA_UPLOAD_MAX_MEMORY_SIZE",
    10 * 1024 * 1024,
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = env_int(
    "DATA_UPLOAD_MAX_NUMBER_FIELDS",
    5000,
)


# =========================
# EMAIL SETTINGS - BREVO SMTP/API READY
# =========================
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp-relay.brevo.com")

EMAIL_PORT = env_int("EMAIL_PORT", 587)

EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER or "no-reply@vetrifresh.com",
)

SERVER_EMAIL = DEFAULT_FROM_EMAIL

CONTACT_RECEIVER_EMAIL = os.getenv(
    "CONTACT_RECEIVER_EMAIL",
    "padmavathyparasanna4@gmail.com",
)

# For Brevo API contact email sending.
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")


# =========================
# CASHFREE PAYMENT SETTINGS
# =========================
CASHFREE_ENV = os.getenv("CASHFREE_ENV", "sandbox")

CASHFREE_CLIENT_ID = os.getenv("CASHFREE_CLIENT_ID", "")

CASHFREE_CLIENT_SECRET = os.getenv("CASHFREE_CLIENT_SECRET", "")

CASHFREE_API_VERSION = os.getenv("CASHFREE_API_VERSION", "2025-01-01")

CASHFREE_NOTIFY_URL = os.getenv("CASHFREE_NOTIFY_URL", "")

if CASHFREE_ENV.lower() == "production":
    CASHFREE_BASE_URL = "https://api.cashfree.com/pg"
else:
    CASHFREE_BASE_URL = "https://sandbox.cashfree.com/pg"


# =========================
# FRONTEND / BACKEND URLS
# =========================
BACKEND_URL = os.getenv("BACKEND_URL", "").strip().rstrip("/")

SITE_URL = FRONTEND_URL or BACKEND_URL


# =========================
# LOGGING
# =========================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },

    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
