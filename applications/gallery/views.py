from django.shortcuts import render

from wagtail.models import Collection
from gallery.models import CustomImage


# def gallery_listing_view(request, group):

#     if group == "grupamlodsza":
#         collections = Collection.objects.filter(name="grupa młodsza")
#     elif group == "grupastarsza":
#         collections = Collection.objects.filter(name="grupa starsza")
#     context = {"galleries": [col.get_children() for col in collections]}
#     return render(request, 'gallery/gallery_listing_page.html', context)


# def gallery_detail_view(request, gallery_id):
#     gallery = CustomImage.objects.filter(collection_id=gallery_id)
#     context = {"gallery": gallery}
#     return render(request, 'gallery/gallery_detail_page.html', context)
