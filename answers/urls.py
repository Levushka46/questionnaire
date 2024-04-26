from django.urls import path

from . import views


urlpatterns = [
    path("", views.page_dev, name="page_dev"),
]
