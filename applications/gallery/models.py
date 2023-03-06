from django.db import models
from django.shortcuts import render

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Collection
from wagtail.images.models import Image, AbstractImage, AbstractRendition


class CustomImage(AbstractImage):
    alt_descr = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="opis alternatywny",
        help_text="Opis zdjęcia (najczęściej od 5 do 15 słów) mający na celu umożliwienie przekazu treści osobom z niepełnosprawnością.",
    )
    admin_form_fields = Image.admin_form_fields + ("alt_descr",)


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class GalleryListingPage(RoutablePageMixin, Page):
    template = "gallery/gallery_listing_page.html"
    max_count = 1
    subpage_types = ["gallery.GalleryDetailPage"]
    password_required_template = "gallery/password_required.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        group = request.GET.get("group")

        if group == "grupamlodsza":
            collections = Collection.objects.filter(name="grupa młodsza")
            context["group"] = "grupa młodsza"
        elif group == "grupastarsza":
            collections = Collection.objects.filter(name="grupa starsza")
            context["group"] = "grupa starsza"
        else:
            collections = []

        galleries = [col.get_children() for col in collections]

        obj_list = []
        for item in galleries:
            for i in item:
                image = CustomImage.objects.filter(collection_id=i.id).last()
                i.__dict__["image"] = image
                obj_list.append(i)
        obj_list = sorted(obj_list, key=lambda p: getattr(p, "id"), reverse=True)
        context["galleries"] = obj_list
        return context


class GalleryDetailPage(Page):
    """Parental gallery detail page."""

    template = "gallery/gallery_detail_page.html"
    max_count = 1
    subpage_types = []
    parent_page_types = ["gallery.GalleryListingPage"]
    password_required_template = "gallery/password_required.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if request.GET.get("gallery_id", None):
            gallery_id = request.GET.get("gallery_id")
            gallery = CustomImage.objects.filter(collection_id=gallery_id)
            collection = Collection.objects.get(id=gallery_id)
            context["group"] = collection.get_parent()
            context["gallery"] = gallery
            context["collection"] = collection
            print(context)
        return context
