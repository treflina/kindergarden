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
    alt_attr = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="opis alternatywny"
    )
    panels = [FieldPanel("home_gallery_image"), FieldPanel("alt_attr")]


class HomePageAccordion(Orderable):
    """News accordion content"""

    page = ParentalKey("home.HomePage", related_name="accordion")
    news_heading = models.CharField(
        max_length=100, null=True, blank=False, verbose_name="nagłówek"
    )
    news_text = RichTextField(
        features=["bold", "italic", "ol", "ul", "link", "hr"], verbose_name="treść"
    )
    panels = [FieldPanel("news_heading"), FieldPanel("news_text")]


class HomePage(RoutablePageMixin, Page):
    """Home page model."""

    template = "home/home_page.html"
    max_count = 1

    month_num = date.today().month
    accordion_content = StreamField(
        [
            ("title_text_and_table", blocks.TitleTextAndTableBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        verbose_name="Aktualności",
    )

    content_panels = Page.content_panels + [
        FieldPanel("accordion_content"),
        MultiFieldPanel(
            [
                InlinePanel(
                    "home_gallery_images", max_num=14, min_num=14, label="Zdjęcie"
                )
            ],
            heading="Galeria na stronie głównej",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["month"] = self.month_num
        return context

    @route(
        r"^(?P<group_slug>[-\w]*)/tematyka/(?P<month_slug>[-\w]*)/$",
        name="thematic_view",
    )
    def thematic_view(self, request, group_slug=None, month_slug=None):
        """Find thematic page based on slugs."""

        context = self.get_context(request)

        try:
            month = MonthFilter.objects.get(slug=month_slug)
            month_num = str(int(month_slug) - 1)
        except (AttributeError, MonthFilter.DoesNotExist) as ex:
            month_slug = None
            return render(request, "404.html")

        try:
            group = GroupsFilter.objects.get(slug=group_slug)
        except (AttributeError, GroupsFilter.DoesNotExist):
            group_slug = None
            return render(request, "404.html")

        if group_slug is not None and month_slug is not None:
            thematic_page = (
                ThematicPage.objects.live()
                .filter(group_id=group.id, month_id=month.id)
                .last()
            )
        else:
            return render(request, "404.html")

        context["thematic_page"] = thematic_page
        context["month_num"] = month_slug
        context["group_choice"] = group_slug
        print(context)

        return render(request, "thematic/thematic_page.html", context)
