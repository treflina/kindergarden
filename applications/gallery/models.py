from PIL import Image as PILImage
from io import BytesIO

from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ForeignKey
from wagtail.models import Page, Orderable, Collection
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from applications.thematic.models import GroupsFilter


class CustomImage(AbstractImage):
    alt_descr = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="opis alternatywny",
        help_text="Opis zdjęcia (najczęściej od 5 do 15 słów) mający na celu umożliwienie przekazu treści osobom z niepełnosprawnością.",
    )
    admin_form_fields = Image.admin_form_fields + ("alt_descr",)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        if self.width > 1200 or self.height > 1200:
            img = PILImage.open(self.file.path)
            img.thumbnail((1200, 1200))
            width, height = img.size
            img.save(self.file.path)

            if self.width != width or self.height != height:
                self.width = width
                self.height = height
                self.file_size = self.file.size
                self.save(update_fields=["width", "height", "file_size"])


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class GalleryListingPage(Page):

    template = "gallery/gallery_listing_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["gallery.GalleryDetailPage"]
    password_required_template = "gallery/password_required.html"

    def get_context(self, request, *args, **kwargs):

        context = super().get_context(request, *args, **kwargs)
        galleries = (
            GalleryListingPage.get_children(self)
            .specific()
            .live()
            .order_by("-first_published_at")
        )
        context["galleries"] = galleries
        return context

    class Meta:
        verbose_name = "Galeria - strona nadrzędna"


class GalleryDetailPage(Page):

    template = "gallery/gallery_detail_page.html"
    subpage_types = []
    parent_page_types = ["gallery.GalleryListingPage"]
    password_required_template = "gallery/password_required.html"

    content_panels = Page.content_panels + [
        MultipleChooserPanel(
            "gallery_images",
            label="Zdjęcia",
            chooser_field_name="image",
        )
    ]

    class Meta:
        verbose_name = "Galeria zdjęć"


class GalleryImage(Orderable):

    page = ParentalKey(
        GalleryDetailPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="+", verbose_name="zdjęcie"
    )

    panels = [
        FieldPanel("image"),
    ]
