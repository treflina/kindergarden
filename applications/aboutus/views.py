from django.shortcuts import render


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
    return render(
        request, "aboutus/sitemap.html", context={"page_title": "Mapa strony"}
    )

def regulations(request):
    return render(request, "aboutus/regulations.html", {"page_title": "Regulamin"})


def statut(request):
    return render(request, "aboutus/statut.html", {"page_title": "Statut"})

def rodo(request):
    return render(request, "aboutus/rodo.html", {"page_title": "Rodo"})
