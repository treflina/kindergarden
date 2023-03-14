from django.shortcuts import render

from wagtail.models import Collection
from wagtail.documents.models import Document

from utils import convert_bytes, extract_extension


def general(request):
    todownload = Document.objects.filter(collection__name="dyrektor").order_by("created_at")
    title = "Rekrutacja i inne dokumenty"
    for doc in todownload:
        doc.file_size_converted = convert_bytes(doc.file_size)
        doc.type = extract_extension(doc.file)

    context = {"todownload": todownload, "page_title": "Do pobrania", "title": title}
    return render(request, "todownload/todownload.html", context)


def teachers(request):
    todownload = Document.objects.filter(collection__name="nauczyciele")
    title = "Materiały od nauczycieli"
    for doc in todownload:
        doc.file_size_converted = convert_bytes(doc.file_size)
        doc.type = extract_extension(doc.file)

    context = {"todownload": todownload, "page_title": "Do pobrania", "title": title}
    return render(request, "todownload/todownload.html", context)


def speechtherapist(request):
    todownload = Document.objects.filter(collection__name="logopeda")
    title = "Materiały od logopedy"
    for doc in todownload:
        doc.file_size_converted = convert_bytes(doc.file_size)
        doc.type = extract_extension(doc.file)

    context = {"todownload": todownload, "page_title": "Do pobrania", "title": title}
    return render(request, "todownload/todownload.html", context)
