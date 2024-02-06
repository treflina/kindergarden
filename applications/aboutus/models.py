from django.db import models
from django import forms

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.table_block.blocks import TableBlock

from home.blocks import custom_table_options
from .blocks import ScheduleBlock


class AboutUsIndexPage(Page):
    template = "aboutus/about_us_index_page.html"
    parent_page_types = ["home.HomePage"]
    max_count = 1

    class Meta:
        verbose_name = "Zakładka 'O nas'"


class CustomPage(Page):
    template = "aboutus/custom_page.html"

    body = RichTextField(
        features=[
            "h2",
            "h3",
            "bold",
            "italic",
            "ol",
            "ul",
            "hr",
            "text-green",
            "text-violet",
            "text-violetlight",
            "text-red",
            "text-blue",
            "link",
            "document-link",
            "image",
            "blockquote",
        ],
        verbose_name="Treść strony",
    )
    table = StreamField(
        [
            (
                "table",
                TableBlock(
                    required=False,
                    label="Tabela",
                    template="home/table_block.html",
                    table_options=custom_table_options,
                ),
            )
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("table"),
    ]

    class Meta:
        verbose_name = "Nowa strona"


class ConceptPage(Page):
    template = "aboutus/concept.html"
    subpage_types = []
    parent_page_types = ["aboutus.AboutUsIndexPage"]
    max_count = 1

    class Meta:
        verbose_name = "Koncepcja pracy przedszkola (nie do edycji)"


class StatusPage(Page):
    template = "aboutus/statut.html"
    subpage_types = []
    parent_page_types = ["aboutus.AboutUsIndexPage"]
    max_count = 1

    class Meta:
        verbose_name = "Statut (nie do edycji)"


class SchedulePage(Page):
    template = "aboutus/schedule.html"
    subpage_types = []
    parent_page_types = ["aboutus.AboutUsIndexPage"]
    max_count = 1

    group_1 = StreamField([("activity", ScheduleBlock())], use_json_field=True, verbose_name="Grupa młodsza", null=True)
    group_2 = StreamField([("acticity", ScheduleBlock())], use_json_field=True, verbose_name="Grupa starsza", null=True)

    content_panels = Page.content_panels + [
        FieldPanel("group_1"),
        FieldPanel("group_2"),
    ]

    class Meta:
        verbose_name = "Rozkład dnia"


class AccessibilityInfoPage(Page):
    template = "aboutus/accessibility.html"
    subpage_types = []
    max_count = 1

    publication_date = models.DateField(
        verbose_name="Data publikacji strony internetowej", blank=False
    )
    update_date = models.DateField(verbose_name="Data ostatniej istotnej aktualizacji", blank=True)
    accordance = models.BooleanField("Zgodność z ustawą", blank=False, default=False )
    exceptions = RichTextField(
        "Niezgodności z ustawą, wyłączenia",
        help_text="Wypełnij w przypadku częściowej zgodności z ustawą",
        features=["bold", "italic", "ol", "ul", "hr"], blank=True, null=True
    )
    publish_date = models.DateField(verbose_name="Data sporządzenia deklaracji", blank=False)
    review_date = models.DateField(verbose_name="Data ostatniego przeglądu deklaracji", blank=False)
    contact_person = models.CharField(verbose_name="Osoba do kontaktu", max_length=50, blank=False)
    email = models.EmailField("Email", blank=False)
    phone = models.CharField("Telefon", max_length=30, blank=False)
    architecture_desc = RichTextField(
        "Opis dostępności architektonicznej",
        features=["bold", "italic", "ol", "ul", "hr"], blank=False
    )
    contact_methods = RichTextField(
        "Komunikacja osób niesłyszących lub słabo słyszących", blank=True, null=True,
        features=["bold", "italic", "ol", "ul", "hr"],
    )

    content_panels = Page.content_panels + [
        FieldPanel("publication_date"),
        FieldPanel("update_date"),
        FieldPanel("accordance", widget=forms.RadioSelect(choices=[(True, "pełna"), (False, "częściowa")])),
        FieldPanel("exceptions"),
        FieldPanel("publish_date"),
        FieldPanel("review_date"),
        FieldPanel("contact_person"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("architecture_desc"),
        FieldPanel("contact_methods"),
    ]

    class Meta: # noqa
        verbose_name = "Deklaracja dostępności"
