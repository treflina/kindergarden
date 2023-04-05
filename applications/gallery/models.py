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
        if self.width > 1500:
            img = PILImage.open(self.file.path)
            img.thumbnail((1500, 1500))
            width, height = img.size
            img.save(self.file.path)

            if  self.width != width or self.height != height:
                self.width = width
                self.height = height
                self.file_size = self.file.size
                self.save(update_fields=["width", "height", "file_size"])

            # img = BytesIO(self.file.read())
            # pil_img = PILImage.open(img)
            # pil_img.thumbnail((100,100))
            # width, height = pil_img.size
            # pil_img.seek(0)
            # pil_img.save(img, format='JPEG')


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class GalleryListingPage(RoutablePageMixin, Page):
    template = "gallery/gallery_listing_page.html"

    subpage_types = ["gallery.GalleryDetailPage", "gallery.GalleryDetailPage2"]
    password_required_template = "gallery/password_required.html"

    class Meta:
        verbose_name = "Galeria - strona nadrzędna"

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

    subpage_types = []
    parent_page_types = ["gallery.GalleryListingPage"]
    password_required_template = "gallery/password_required.html"

    class Meta:
        verbose_name = "Galeria zdjęć"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if request.GET.get("gallery_id", None):
            gallery_id = request.GET.get("gallery_id")
            gallery = CustomImage.objects.filter(collection_id=gallery_id)
            collection = Collection.objects.get(id=gallery_id)
            context["group"] = collection.get_parent()
            context["gallery"] = gallery
            context["collection"] = collection
        return context





class GalleryDetailPage2(Page):

    template = "gallery/gallery_detail_page.html"
    subpage_types = []
    parent_page_types = ["gallery.GalleryListingPage"]
    password_required_template = "gallery/password_required.html"

    group = models.ForeignKey(
        "thematic.GroupsFilter",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="grupa",
    )

    content_panels = Page.content_panels + [
        MultipleChooserPanel(
            'gallery_images',
            label="Gallery images",
            chooser_field_name="image",
        ),
        FieldPanel('group'),
    ]

class BlogPageGalleryImage(Orderable):
    """
    Example related image
    """

    page = ParentalKey(GalleryDetailPage2, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name='+'
    )


    panels = [
        FieldPanel('image'),
    ]


