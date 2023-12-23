from django.db import models
from wagtail.blocks import StructValue, StructBlock, ChoiceBlock, PageChooserBlock


GALLERY_LINKS_NAMES_CHOICES = (
    ("0", "Zobacz więcej zdjęć"),
    ("1", "Zobacz więcej zdjęć w gr. młodszej"),
    ("2", "Zobacz więcej zdjęć w gr. starszej"),
)

GALLERY_LINKS_NAMES_CHOICES_LOOKUP = dict(GALLERY_LINKS_NAMES_CHOICES)


class LinkStructValue(StructValue):
    def url(self):
        page = self.get("page")
        return page.url


class PhotogalleryLinkBlock(StructBlock):
    label = ChoiceBlock(
        label="Tekst przycisku prowadzącego do fotogalerii.",
        choices=GALLERY_LINKS_NAMES_CHOICES,
        icon="view",
        required=True,
    )
    photogallery = PageChooserBlock(
        label="fotogaleria",
        page_type=[
            "gallery.PhotogalleryDetailPage2",
            "gallery.PhotogalleryDetailPage",
        ],
        required=True,
    )

    # @property
    # def label_display(self):
    #     return "hmm"

    class Meta:
        value_class = LinkStructValue
