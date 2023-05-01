from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


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
            "link",
            "document-link",
            "image",
            "blockquote",
        ],
        verbose_name="Treść strony",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
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

    class Meta:
        verbose_name = "Rozkład dnia (nie do edycji)"
