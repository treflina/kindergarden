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

import home


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
        help_text="Slug znajduje się w adresie strony internetowej po ukośniku. Proszę użyć liczby np. dla czerwca '6'",
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
        help_text="Slug znajduje się w adresie strony internetowej po ukośniku. Proszę wpisać 'grupamlodsza' lub 'grupastarsza'",
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

class ThematicIndexPage(Page):
    """Parent page for thematic pages"""

    template = "thematic/thematic_index_page.html"
    subpage_types = ["thematic.ThematicPage"]
    parent_page_types = ["home.HomePage"]

    class Meta:
        verbose_name = "Tematyka - strona nadrzędna"


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        month_num = date.today().month
        if request.GET.get("group", None):
            group = str(request.GET.get("group"))
            month = str(request.GET.get("month", month_num))
            obj = ThematicPage.objects.filter(group__slug=group, month__slug=month).last()
            context["thematic_page"] = obj
            context["month_num"] = month
            context["group_choice"] = group

        return context


class ThematicPage(Page):
    """Thematic detail page model."""

    subpage_types = []
    parent_page_types = ["thematic.ThematicIndexPage"]

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

    class Meta:
        verbose_name = "Tematyka na dany miesiąc"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["month_num"] = str(date.today().month)
        return context
