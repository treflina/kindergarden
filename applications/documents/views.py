from django.shortcuts import render

from wagtail.models import Collection
from wagtail.documents.models import Document

from utils import convert_bytes, extract_extension


def general(request):
    documents = Document.objects.filter(collection__name="dyrektor")
    for doc in documents:
        doc.file_size_converted = convert_bytes(doc.file_size)
        doc.type = extract_extension(doc.file)

    context = {"documents": documents}
    return render(request, "documents/documents.html", context)


def teachers(request):
    return render(request, "documents/documents.html")


def speechtherapist(request):
    return render(request, "documents/documents.html")
