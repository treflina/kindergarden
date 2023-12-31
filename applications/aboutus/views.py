from django.shortcuts import render

from applications.thematic.models import ThematicIndexPage
from applications.chronicle.models import ChronicleIndexPage
from .models import AboutUsIndexPage


def concept(request):
    return render(
        request, "aboutus/concept.html", context={"page_title": "Koncepcja pracy"}
    )


def contact(request):
    return render(request, "aboutus/contact.html", context={"page_title": "Kontakt"})


def payments(request):
    return render(
        request, "aboutus/payments.html", context={"page_title": "Opłaty i konto"}
    )


def procedures(request):
    return render(
        request, "aboutus/procedures.html", context={"page_title": "Procedury"}
    )


def schedule(request):
    return render(
        request, "aboutus/schedule.html", context={"page_title": "Rozkład dnia"}
    )


def sitemap(request):
    aboutus_children = AboutUsIndexPage.objects.last().get_children().specific()

    chronicle_index_page = ChronicleIndexPage.objects.live().last()

    thematic_page1 = ThematicIndexPage.objects.filter(slug="tematyka1").first()
    thematic_page2 = ThematicIndexPage.objects.filter(slug="tematyka2").first()

    if thematic_page1:
        thematic1 = thematic_page1.get_children().live().exists()
    else:
        thematic1 = None

    if thematic_page2:
        thematic2 = thematic_page2.get_children().live().exists()
    else:
        thematic2 = None

    return render(
        request,
        "aboutus/sitemap.html",
        context={
            "page_title": "Mapa strony",
            "aboutus_children": aboutus_children,
            "chronicle_index_page": chronicle_index_page,
            "thematic1": thematic1,
            "thematic2": thematic2,
        },
    )


def regulations(request):
    return render(request, "aboutus/regulations.html", {"page_title": "Regulamin"})


def statut(request):
    return render(request, "aboutus/statut.html", {"page_title": "Statut"})


def rodo(request):
    return render(request, "aboutus/rodo.html", {"page_title": "Rodo"})


def events(request):
    return render(request, "aboutus/events.html", {"page_title": "Kalendarz"})
