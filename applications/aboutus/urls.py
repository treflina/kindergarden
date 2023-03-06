from django.urls import include, path
from . import views

app_name = "aboutus_app"

urlpatterns = [
    path("koncepcja/", views.concept, name="concept"),
    path("oplaty/", views.payments, name="payments"),
    path("regulamin/", views.regulations, name="regulations"),
    path("rozklad/", views.schedule, name="schedule"),
    path("procedury/", views.procedures, name="procedures"),
    path("kontakt/", views.contact, name="contact"),
    path("mapastrony/", views.sitemap, name="sitemap"),
]
