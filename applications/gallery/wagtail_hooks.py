from wagtail import hooks

from .views import images_chooser_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return images_chooser_viewset