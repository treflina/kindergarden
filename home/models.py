from datetime import date

from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.http import Http404, JsonResponse

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
from wagtail.snippets.models import register_snippet
from applications.thematic.models import (
    MonthFilter,
    GroupsFilter,
    ThematicPage,
    ThematicIndexPage,
)
from applications.gallery.models import GalleryListingPage, CustomImage
from applications.chronicle.models import ChroniclePage, ChronicleIndexPage
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


class HomePage(Page):
    """Home page model."""

    template = "home/home_page.html"
    ajax_template = "home/chronicle_posts.html"
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
        context["events"] = EventSnippet.objects.all().order_by("date")
        context["month"] = self.month_num

        thematic_page1 = ThematicIndexPage.objects.filter(slug="tematyka1").first()
        thematic_page2 = ThematicIndexPage.objects.filter(slug="tematyka2").first()

        if thematic_page1:
            context["thematic1"] = thematic_page1.get_children().live().exists()

        if thematic_page2:
            context["thematic2"] = thematic_page2.get_children().live().exists()

        context["chronicle_index_page"] = ChronicleIndexPage.objects.live().last()

        chronicle_posts = (
            ChroniclePage.objects.live()
            .specific()
            .order_by("-publish_date", "-first_published_at")
        )

        paginator = Paginator(chronicle_posts, 3)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        return context


class EventSnippet(models.Model):
    date = models.DateField(verbose_name="Data")
    description = models.TextField(verbose_name="Opis wydarzenia")

    panels = [
        FieldPanel("date"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"

    def __str__(self):
        return f"{self.date}: {self.description}"

    @property
    def is_past(self):
        return date.today() > self.date


register_snippet(EventSnippet)
