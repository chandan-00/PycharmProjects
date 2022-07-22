from django.urls import path

from . import views

urlpatterns = [
    path("show/<int:id>/", views.index, name="index"),
    path("", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("show/", views.show, name="show"),
]
