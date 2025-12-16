import os
import json
import mimetypes
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


with open(os.path.join(BASE_DIR, "secret.json")) as f:
    secret = json.loads(f.read())


def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = f"Nie mam dostępu do zmiennej {secret_name}"
        raise ImproperlyConfigured(msg)


DEBUG = get_secret("DEBUG")

ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")

SECRET_KEY = get_secret("SECRET_KEY")
GOOGLE_MAP_API_KEY = get_secret("GOOGLE_MAP_API_KEY")


# Application definition

INSTALLED_APPS = [
    "home",
    "search",
    "applications.thematic",
    "applications.aboutus",
    "applications.todownload",
    "applications.gallery",
    "applications.menus",
    "applications.chronicle",
    #
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    # "wagtail.images",
    "applications.gallery.apps.GalleryImagesAppConfig",
    "wagtail_multi_upload",
    "wagtail.search",
    "wagtail.admin",
    "wagtail_draftail_anchors",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail",
    "wagtail.contrib.table_block",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_extensions",
    "corsheaders",
    "robots",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "przedszkole.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "home.utils.context_processors.todownloadpages_context",
            ],
            "libraries": {
                "env_extras": "applications.aboutus.templatetags.env_extras",
            },
        },
    },
]

WSGI_APPLICATION = "przedszkole.wsgi.application"

# if DEBUG:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }

# else:
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_secret("DB_NAME"),
        "USER": get_secret("DB_USER"),
        "PASSWORD": get_secret("DB_PASSWORD"),
        "HOST": get_secret("DB_HOST"),
        "PORT": "",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pl"

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if get_secret("DEVIL"):
    STATIC_ROOT = os.path.join(BASE_DIR, "public", "static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "public", "media")
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "/static/"
MEDIA_URL = "/media/"


# Wagtail settings

WAGTAIL_SITE_NAME = "przedszkole"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"
WAGTAILIMAGES_IMAGE_MODEL = "gallery.CustomImage"
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 10 * 1024 * 1024
WAGTAILDOCS_SERVE_METHOD = "serve_view"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CSRF_TRUSTED_ORIGINS = get_secret("CSRF_TRUSTED_ORIGINS")
# CORS_ALLOWED_ORIGINS = get_secret("CORS_ALLOWED_ORIGINS")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "WARN", "handlers": ["file"]},
    "handlers": {
        "file": {
            "level": "WARN",
            "class": "logging.FileHandler",
            "filename": "django.log",
            "formatter": "app",
        },
    },
    "loggers": {
        "django": {"handlers": ["file"], "level": "WARN", "propagate": True},
    },
    "formatters": {
        "app": {
            "format": (
                "%(asctime)s [%(levelname)-8s] " "(%(module)s.%(funcName)s) %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}

sentry_sdk.init(
    dsn=get_secret("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
