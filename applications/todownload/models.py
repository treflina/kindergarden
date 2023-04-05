from django.db import models
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from modelcluster.fields import ParentalKey, ForeignKey
from wagtail.models import Page, Orderable, Collection
from wagtail.documents.models import Document
from wagtail.admin.panels import FieldPanel, MultipleChooserPanel

from utils import extract_extension, convert_bytes


class ToDownloadPage(Page):

    template = "todownload/todownload_page.html"
    subpage_types = []
    parent_page_types = ["home.HomePage"]


    heading = models.CharField(max_length=30, verbose_name="nagłówek", default='')

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        MultipleChooserPanel(
            'todownload_documents',
            label="Materiały i dokumenty",
            chooser_field_name="document",
        ),
    ]

class ToDownloadDocument(Orderable):

    page = ParentalKey(ToDownloadPage, on_delete=models.CASCADE, related_name='todownload_documents')
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='+'
    )

    @property
    def get_extension(self):
        return extract_extension(self.document.file)

    @property
    def get_size(self):
        return convert_bytes(self.document.file_size)


    panels = [
        FieldPanel('document'),
    ]