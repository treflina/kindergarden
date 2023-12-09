from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.images.views.chooser import ImageChooserViewSet


class MyChooserViewSet(ChooserViewSet):
    per_page = 25
    ordering = ("id",)

class CustomImageChooserViewSet(ImageChooserViewSet, MyChooserViewSet):
    pass

images_chooser_viewset = CustomImageChooserViewSet(
    "images_chooser",
    url_prefix="images/chooser"
)
