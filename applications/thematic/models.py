from datetime import date
from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet


class ThematicContentOrderable(Orderable):
    """This allows us to select one or more blog authors from Snippets."""

    page = ParentalKey("thematic.ThematicPage", related_name="thematic_content")
    heading = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        default="np. Nasze ważne dni",
        verbose_name="podtytuł",
    )
    text_content = RichTextField(
        verbose_name="treść", features=["bold", "italic", "ol", "ul", "link", "hr"]
    )

    panels = [FieldPanel("heading"), FieldPanel("text_content")]


class MonthFilter(models.Model):
    """Snippet used to filter pages according to months"""

    name = models.CharField(max_length=50, verbose_name="nazwa")
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=50,
        help_text="Slug znajduje się w adresie strony internetowej po ukośniku",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "miesiąc"
        verbose_name_plural = "miesiące"

    def __str__(self):
        return self.name


register_snippet(MonthFilter)


class GroupsFilter(models.Model):
    """Snippet used to filter content according to groups."""

    name = models.CharField(max_length=50, verbose_name="nazwa")
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=50,
        help_text="Slug znajduje się w adresie strony internetowej po ukośniku",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "grupa"
        verbose_name_plural = "grupy"

    def __str__(self):
        return self.name


register_snippet(GroupsFilter)


class ThematicPage(RoutablePageMixin, Page):

    """Thematic detail page model."""

    template = "thematic/thematic_page.html"

    month = models.ForeignKey(
        "thematic.MonthFilter",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="miesiąc",
    )
    group = models.ForeignKey(
        "thematic.GroupsFilter",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="grupa",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("thematic_content", min_num=1, label="Treść")],
            heading="Tematyka zajęć, ważne dni, cele, inne",
        ),
        FieldPanel("group"),
        FieldPanel("month"),
    ]
