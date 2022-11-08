
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/<int:id>/following", views.userFollowing, name="userFollowing"),
    path("profile/<int:id>/followers", views.userFollowers, name="userFollowers"),
    path("following", views.following, name="following"),

    #feth urls
    path("like", views.like, name="like"),
    path("saveEdit", views.saveEdit, name="saveEdit"),
    path("follow", views.follow, name="follow")
]
