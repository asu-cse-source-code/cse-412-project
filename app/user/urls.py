from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_users),
    path("<str:id>", views.get_user),
    path("add/bulk", views.add_users),
    path("user/login", views.login_user),
]
