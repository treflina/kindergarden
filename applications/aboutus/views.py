from django.shortcuts import render


def concept(request):
    return render(request, "aboutus/concept.html")


def contact(request):
    return render(request, "aboutus/contact.html")


def payments(request):
    return render(request, "aboutus/payments.html")


def procedures(request):
    return render(request, "aboutus/procedures.html")


def schedule(request):
    return render(request, "aboutus/schedule.html")


def sitemap(request):
    return render(request, "aboutus/sitemap.html")


def regulations(request):
    return render(request, "aboutus/regulations.html")
