from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_games),
    path("<str:id>", views.get_game),
    path("game/add", views.add_game),
    path("game/add/bulk", views.add_games),
]
