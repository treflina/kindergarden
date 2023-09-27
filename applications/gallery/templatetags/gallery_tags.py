from django import template
from applications.gallery.models import CustomImage

register = template.Library()

@register.inclusion_tag("tags/gallery.html", takes_context=True)
def gallery(context, gallery):

    images = CustomImage.objects.filter(collection=gallery)
    if not images:
        self = context.get("self")
        try:
            images = [img.image1 for img in self.gallery_images1.all()]
        except AttributeError:
            pass
        try:
            images = [img.image2 for img in self.gallery_images2.all()]
        except AttributeError:
            pass

    return {
        "images": images,
        "request": context["request"],
    }