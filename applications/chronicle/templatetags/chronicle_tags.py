from django import template
from applications.chronicle.blocks import GALLERY_LINKS_NAMES_CHOICES_LOOKUP

register = template.Library()


@register.simple_tag
def get_display_name(name):
    return GALLERY_LINKS_NAMES_CHOICES_LOOKUP.get(name)
