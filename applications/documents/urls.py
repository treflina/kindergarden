from django.urls import include, path
from . import views

app_name = "documents_app"

urlpatterns = [
    path("dopobrania/dyrektor", views.general, name="general"),
    path("dopobrania/logopeda", views.speechtherapist, name="speechtherapist"),
    path("dopobrania/nauczyciele", views.teachers, name="teachers"),
]
