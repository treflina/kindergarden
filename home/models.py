from datetime import date

from django.db import models
from django.shortcuts import render
from django.http import Http404

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.fields import ParentalKey

from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.models import Collection
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable
from applications.thematic.models import MonthFilter, GroupsFilter, ThematicPage
from applications.gallery.models import GalleryListingPage, CustomImage

from . import blocks


class HomePageGallery(Orderable):
    """Images for the home page gallery."""

    page = ParentalKey("home.HomePage", related_name="home_gallery_images")
    home_gallery_image = models.ForeignKey(
        # "wagtailimages.Image"
        CustomImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="zdjęcie",
    )

    panels = [
        FieldPanel("home_gallery_image"),
    ]


class HomePage(RoutablePageMixin, Page):
    """Home page model."""

    template = "home/home_page.html"
    max_count = 1

    month_num = date.today().month
    accordion_content = StreamField(
        [
            ("news", blocks.AccordionBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name="Aktualności",
    )
    groups = StreamField(
        [("group_definition", blocks.GroupsNameAndImageBlock())],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name="Grupy",
    )

    content_panels = Page.content_panels + [
        FieldPanel("accordion_content"),
        MultiFieldPanel(
            [InlinePanel("home_gallery_images", label="Zdjęcie")],
            heading="Galeria na stronie głównej (14 zdjęć - na duży ekran, zdjęcia nr 2, 5, 13 wykorzystane są na mały ekran)",
        ),
        FieldPanel("groups"),
    ]

    class Meta:
        verbose_name = "Strona główna"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["month"] = self.month_num
        return context
