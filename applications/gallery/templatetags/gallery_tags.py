from django import template
from applications.gallery.models import CustomImage

register = template.Library()

@register.inclusion_tag("tags/gallery.html", takes_context=True)
def gallery(context, gallery):

    images = CustomImage.objects.filter(collection=gallery)
    if not images:
        self = context.get("self")
        images = [img.image for img in self.gallery_images.all()]

    return {
        "images": images,
        "request": context["request"],
    }