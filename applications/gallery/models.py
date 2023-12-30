from PIL import Image as PILImage
from io import BytesIO

from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q

from modelcluster.fields import ParentalKey, ForeignKey
from wagtail.models import Page, Orderable, Collection
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    FieldRowPanel,
    MultipleChooserPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail_multi_upload.edit_handlers import MultipleImagesPanel

from applications.thematic.models import GroupsFilter


class CustomImage(AbstractImage):
    alt_descr = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="opis alternatywny",
        help_text="Opis zdjęcia (najczęściej od 5 do 15 słów) mający na celu umożliwienie przekazu treści osobom z niepełnosprawnościami.",
    )
    priority = models.BooleanField(
        default=False,
        verbose_name="wyróżnienie zdjęcia",
        help_text="Zdjęcie wyróżnione wyświetla się jako zdjęcie główne galerii.",
    )
    admin_form_fields = Image.admin_form_fields + (
        "alt_descr",
        "priority",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (
            self.width > 1200 or self.height > 1200
            ) and self.collection.name != "Zdjęcia - rozmiar oryginalny":
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


class GalleryListingPage(RoutablePageMixin, Page):
    template = "gallery/gallery_listing_page.html"
    max_count = 1
    subpage_types = ["gallery.GalleryDetailPage"]
    password_required_template = "gallery/password_required.html"

    class Meta:
        verbose_name = "Galeria - strona nadrzędna"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        group = request.GET.get("group")

        try:
            if group == "1":
                collections = Collection.objects.filter(
                    Q(name="grupa młodsza") | Q(name="Grupa młodsza")
                )
                context["group"] = "- grupa młodsza"
            elif group == "2":
                collections = Collection.objects.filter(
                    Q(name="grupa starsza") | Q(name="Grupa starsza")
                )
                context["group"] = "- grupa starsza"
            else:
                collections = []
                context["group"] = ""
        except:
            raise Http404

        galleries = [col.get_children() for col in collections]
        obj_list = []
        for item in galleries:
            for i in item:
                image = CustomImage.objects.filter(
                    (Q(collection_id=i.id) & Q(priority=True))
                ).last()
                if image is None:
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

    class Meta:
        verbose_name = "Galeria zdjęć"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if request.GET.get("gallery_id", None):
            gallery_id = request.GET.get("gallery_id")
            gallery = CustomImage.objects.filter(collection_id=gallery_id).order_by(
                "id"
            )
            collection = get_object_or_404(Collection, id=gallery_id)
            context["group"] = collection.get_parent().name.lower()
            context["gallery"] = gallery
            context["collection"] = collection
        return context


class PhotogalleryListingPage(Page):
    template = "gallery/photogallery_listing_page.html"
    max_count = 2
    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "gallery.PhotogalleryDetailPage",
        "gallery.PhotogalleryDetailPage2",
    ]
    password_required_template = "gallery/password_required.html"

    class Meta:
        verbose_name = "Lista fotogalerii"

    group = models.ForeignKey(
        GroupsFilter,
        verbose_name="Grupa",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
    )
    content_panels = Page.content_panels + [
        FieldPanel("group", heading="Grupa"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        galleries = (
            self.get_children().live().specific().order_by("-first_published_at")
        )
        context["galleries"] = galleries
        return context


class PhotogalleryDetailPage(Page):
    page_description = "Zdjęcia zostaną wgrane."
    template = "gallery/photogallery_detail_page.html"
    subpage_types = []
    parent_page_types = ["gallery.PhotogalleryListingPage"]
    password_required_template = "gallery/password_required.html"

    collection = models.ForeignKey(
        Collection,
        verbose_name="Kolekcja zdjęć",
        # limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    @property
    def image(self):
        # if self.collection:
        #     image = CustomImage.objects.filter(Q(collection_id=self.collection.id)&Q(priority=True)).last()
        #     if image is None:
        #         image = CustomImage.objects.filter(Q(collection_id=self.collection.id)).last()
        # else:
        # image_obj = self.gallery_images.filter(image__priority=True).last() | self.gallery_images.all().last()
        # image = image_obj.image
        # return image

        image_obj = self.gallery_images1.filter(highlight=True).last()
        if image_obj:
            return image_obj.image1
        else:
            return self.gallery_images1.all().last().image1

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                MultipleImagesPanel(
                    "gallery_images1",
                    image_field_name="image1",
                    label="",
                    help_text="""Pamiętaj o wybraniu kolekcji przed wgrywaniem zdjęć""",
                )
            ],
            heading="Zdjęcia",
        ),
        # FieldPanel("collection"),
    ]

    class Meta:
        verbose_name = "Fotogaleria"


class PhotogalleryDetailPage2(Page):
    page_description = "Zdjęcia są już wgrane na serwerze."
    template = "gallery/photogallery_detail_page.html"
    subpage_types = []
    parent_page_types = ["gallery.PhotogalleryListingPage"]
    password_required_template = "gallery/password_required.html"

    collection = models.ForeignKey(
        Collection,
        verbose_name="Kolekcja zdjęć",
        # limit_choices_to=~models.Q(name__in=["Root"]),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    @property
    def image(self):
        if self.collection:
            image = CustomImage.objects.filter(
                Q(collection_id=self.collection.id) & Q(priority=True)
            ).last()
            if image is None:
                image = CustomImage.objects.filter(
                    Q(collection_id=self.collection.id)
                ).last()
            return image
        else:
            image_obj = self.gallery_images2.filter(highlight=True).last()
            if image_obj:
                return image_obj.image2
            else:
                return self.gallery_images2.all().last().image2

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                MultipleChooserPanel(
                    "gallery_images2",
                    chooser_field_name="image2",
                    label="",
                    help_text="""UWAGA! Wybrane zdjęcia będą widoczne na stronie tylko, jeżeli nie zostanie wybrana cała kolekcja poniżej.""",
                )
            ],
            heading="Zdjęcia",
        ),
        FieldPanel("collection"),
    ]

    class Meta:
        verbose_name = "Fotogaleria2"


class GalleryImageModel1(Orderable):
    page = ParentalKey(
        PhotogalleryDetailPage, on_delete=models.CASCADE, related_name="gallery_images1"
    )

    image1 = models.ForeignKey(
        "CustomImage",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="",
        null=True,
    )
    highlight = models.BooleanField(
        default=False,
        verbose_name="Zdjęcie główne",
        help_text="""Wybrane zdjęcie będzie wyświetlone w wizytówce galerii""",
    )

    panels = [
        FieldRowPanel([FieldPanel("image1"), FieldPanel("highlight")]),
    ]

    def __str__(self):
        return self.image.title


class GalleryImageModel2(Orderable):
    page = ParentalKey(
        PhotogalleryDetailPage2,
        on_delete=models.CASCADE,
        related_name="gallery_images2",
    )

    image2 = models.ForeignKey(
        "CustomImage",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="",
        null=True,
    )
    highlight = models.BooleanField(
        default=False,
        verbose_name="Zdjęcie główne",
        help_text="""Wybrane zdjęcie będzie wyświetlone w wizytówce galerii""",
    )

    panels = [
        FieldRowPanel([FieldPanel("image2"), FieldPanel("highlight")]),
    ]

    def __str__(self):
        return self.image.title


class GalleryImageAbstractModel(Orderable):
    image = models.ForeignKey(
        "CustomImage",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="",
        null=True,
    )
    highlight = models.BooleanField(
        default=False,
        verbose_name="Zdjęcie główne",
        help_text="""Wybrane zdjęcie będzie wyświetlone w wizytówce galerii""",
    )

    panels = [
        FieldRowPanel([FieldPanel("image"), FieldPanel("highlight")]),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        return self.image.title


# class GalleryImage1(GalleryImageAbstractModel):

#     page = ParentalKey(
#         PhotogalleryDetailPage, on_delete=models.CASCADE, related_name="gallery_images1")


# class GalleryImage2(GalleryImageAbstractModel):

#       page = ParentalKey(
#         PhotogalleryDetailPage2, on_delete=models.CASCADE, related_name="gallery_images2"
#     )
