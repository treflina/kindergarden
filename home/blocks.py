from wagtail import blocks
from wagtail.templatetags.wagtailcore_tags import richtext
from wagtail.contrib.table_block.blocks import TableBlock


class TitleTextAndTableBlock(blocks.StructBlock):
    """Title, text and table block"""

    title = blocks.CharBlock(
        required=True, help_text="Wpisz nagłówek", label="Nagłówek"
    )
    text = blocks.RichTextBlock(
        required=True,
        help_text="Wpisz tekst",
        label="Treść",
        features=["bold", "italic", "ol", "ul", "link", "document-link", "hr", "image"],
    )
    table = TableBlock(
        required=False, label="Tabela (opcjonalnie)", template="home/table_block.html"
    )

    class Meta:  # noqa
        template = "home/title_and_text_block.html"
        icon = "edit"
        label = "Nagłówek i tekst"
