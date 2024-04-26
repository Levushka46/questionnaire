from django.urls import path

from . import views


urlpatterns = [
    path("", views.sign_in, name="index"),
    path("page_dev/", views.page_dev, name="page_dev"),
    path("page/<int:page_id>/", views.page, name="page"),
]
