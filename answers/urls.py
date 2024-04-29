from django.urls import path

from . import views


urlpatterns = [
    path("", views.SignInView.as_view(), name="index"),
    path("page/<int:page_id>/", views.PageView.as_view(), name="page"),
    path("done/", views.DoneView.as_view(), name="done"),
    path("no_surveys/", views.NoSurveysView.as_view(), name="no_surveys"),
]
