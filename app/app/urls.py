"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    # Frontend paths
    path("", Home.as_view(), name="index"),
    path("profile", Profile.as_view(), name="profile"),
    path("auth", include("django.contrib.auth.urls")),
    path("login", Login.as_view(), name="login"),
    path("logout", Logout.as_view(), name="logout"),
    path("register", Register.as_view(), name="register"),
    path("game/<str:id>", Games.as_view(), name="game"),
    path("notfound", NotFound.as_view(), name="error"),
    # Backend paths
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("gamespot/users/", include("user.urls")),
    path("gamespot/games/", include("game.urls")),
    path("gamespot/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("gamespot/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
