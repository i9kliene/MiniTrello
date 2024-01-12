from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="home", permanent=False)),
    path("home/", views.homePage, name="home"),
    path("about/", views.aboutPage, name="about"),
    path("register/", views.userRegister, name="user-register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path(
        "change-password/<uidb64>/<token>/",
        views.password_change,
        name="change-password",
    ),
    path("reset-password/", views.resetPassword, name="reset-password"),
    path("login/", views.userLogin, name="user-login"),
    path("logout/", views.userLogout, name="user-logout"),
]
