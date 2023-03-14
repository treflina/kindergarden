from django.apps import AppConfig
from wagtail.images.apps import WagtailImagesAppConfig


class GalleryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications.gallery"


class GalleryImagesAppConfig(WagtailImagesAppConfig):
    default_attrs = {"decoding": "async", "loading": "lazy"}