import os
from django import template
from przedszkole.settings import settings

register = template.Library()


@register.simple_tag
def get_env_var(key):
    return settings.GOOGLE_MAP_API_KEY
