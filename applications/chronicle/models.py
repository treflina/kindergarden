from collections import defaultdict

from django.db import models
from django.utils.timezone import now

from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    MultipleChooserPanel,
)
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey, ForeignKey

from .blocks import PhotogalleryLinkBlock
from applications.gallery.models import PhotogalleryDetailPage, PhotogalleryDetailPage2


class ChronicleIndexPage(Page):
    """Chronicle listing page model."""

    template = "chronicle/chronicle_index_page.html"
    subpage_types = ["chronicle.ChroniclePage"]
    parent_page_types = ["home.HomePage"]
    max_count = 1

    header_image = models.ForeignKey(
        "gallery.CustomImage",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Zdjęcie nagłówkowe w tle",
    )

    content_panels = Page.content_panels + [FieldPanel("header_image")]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        subpages = ChroniclePage.objects.live().order_by("-publish_date")
        context["subpages"] = subpages

        school_years = defaultdict(list)
        for s in subpages:
            if s.publish_date.month <= 9:
                school_years[f"{s.publish_date.year-1}/{s.publish_date.year}"].append(s)
            else:
                school_years[f"{s.publish_date.year}/{s.publish_date.year + 1}"].append(
                    s
                )
        context["school_years"] = school_years.items()

        return context

    class Meta:  # noqa
        verbose_name = "Kronika wydarzeń"
        verbose_name_plural = "Kronika wydarzeń"


class ChroniclePage(Page):
    """Detail page for chronicle content."""

    template = "chronicle/chronicle_page.html"
    page_description = "Relacja z wydarzenia"
    subpage_types = []
    parent_page_types = ["chronicle.ChronicleIndexPage"]

    banner_image = models.ForeignKey(
        "gallery.CustomImage",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Zdjęcie główne",
        help_text="""Preferowana orientacja pozioma. Pamiętaj, że tekst zamieszczony
            na zdjęciu jest niedostępny cyfrowo i powinien znaleźć się również w treści
            artykułu (wymóg dostępności stron internetowych instytucji publicznych).""",
    )
    alt_attr = models.TextField(
        blank=False,
        verbose_name="Opis alternatywny",
        help_text="""Opisz co przedstawia zdjęcie główne. Pole nie powinno być puste
        (wymóg dostępności cyfrowej stron internetowych instytucji publicznych).""",
    )
    text = RichTextField(
        blank=False,
        verbose_name="Tekst",
        features=[],
    )
    publish_date = models.DateField(
        blank=True,
        null=True,
        default=now,
        verbose_name="Data",
        help_text="""Data wyświetlana na stronie.""",
    )
    gallery_link = StreamField(
        [
            ("link", PhotogalleryLinkBlock()),
        ],
        verbose_name="Opcjonalnie: Link do galerii zdjęć",
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("publish_date"),
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
                FieldPanel("alt_attr"),
            ],
            heading="Zdjęcie",
        ),
        FieldPanel("text"),
        MultiFieldPanel(
            [
                MultipleChooserPanel(
                    "images",
                    chooser_field_name="image",
                    label="",
                    help_text="""Pamiętaj o dodaniu tagu 'relacja' w 'Edycji obrazu'""",
                )
            ],
            heading="Opjonalnie: Dodatkowe zdjęcia",
        ),
        FieldPanel("gallery_link"),
    ]

    class Meta:  # noqa
        verbose_name = "Relacja z wydarzenia"
        verbose_name_plural = "Relacje z wydarzeń"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if any(
            PhotogalleryDetailPage.objects.live().filter(
                title=block.value["photogallery"]
            ).exists()
            or PhotogalleryDetailPage2.objects.live().filter(
                title=block.value["photogallery"]
            ).exists()
            for block in self.gallery_link
        ):
            context["link_url_exists"] = True

        chronicle_posts = list(
            ChroniclePage.objects.live().specific().order_by("publish_date")
        )

        try:
            p_index = chronicle_posts.index(self)
            if p_index != len(chronicle_posts) - 1:
                context["prev_post"] = chronicle_posts[p_index + 1]

            if p_index != 0:
                context["next_post"] = chronicle_posts[p_index - 1]
        except ValueError:
            pass

        return context


class ChronicleImageModel(Orderable):
    page = ParentalKey(ChroniclePage, on_delete=models.CASCADE, related_name="images")

    image = models.ForeignKey(
        "gallery.CustomImage",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="",
        null=True,
    )

    panels = [
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.image.title
