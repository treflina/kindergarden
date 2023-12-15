from wagtail.blocks import StructValue, StructBlock, ChoiceBlock, PageChooserBlock


class LinkStructValue(StructValue):
    def url(self):
        page = self.get("page")
        return page.url


class PhotogalleryLinkBlock(StructBlock):
    label = ChoiceBlock(
        label="Tekst przycisku prowadzącego do fotogalerii.",
        choices=[
            ("Zobacz więcej zdjęć", "Zobacz więcej zdjęć"),
            (
                "Zobacz więcej zdjęć w gr. młodszej",
                "Zobacz więcej zdjęć w gr. młodszej",
            ),
            (
                "Zobacz więcej zdjęć w gr. starszej",
                "Zobacz więcej zdjęć w gr. starszej",
            ),
        ],
        icon="view",
        required=True,
    )
    photogallery = PageChooserBlock(
        label="fotogaleria",
        page_type=[
            "gallery.PhotogalleryDetailPage2",
            "gallery.PhotogalleryDetailPage",
        ],
        required=True,
    )

    class Meta:
        value_class = LinkStructValue
