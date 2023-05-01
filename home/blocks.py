from wagtail import blocks
from wagtail.templatetags.wagtailcore_tags import richtext
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock

custom_table_options = {"startCols": 4, "language": "pl-PL"}


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
        required=False,
        label="Zamieść tabelę (opcjonalnie)",
        template="home/table_block.html",
        table_options=custom_table_options,
    )

    class Meta:  # noqa
        template = "home/title_and_text_block.html"
        icon = "edit"
        label = "Nagłówek i tekst"

class GroupsNameAndImageBlock(blocks.StructBlock):
    """Block used to define group name with it's logo image"""

    group_name = blocks.CharBlock(max_length=15, required=True, label="Nazwa grupy")
    group_num = blocks.ChoiceBlock(choices=[('1', 'grupa młodsza'), ('2', 'grupa starsza')], label="Wybierz grupę", required=True)
    group_img = ImageChooserBlock(label="Dodaj logo grupy")

    class Meta:  # noqa
        template = "home/groups_block.html"
        icon = "edit"
        label = "Grupa"
