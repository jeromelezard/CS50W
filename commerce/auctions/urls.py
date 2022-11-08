from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path ("watchlist", views.watchlist, name="watchlist"),
    path("user/<int:user_id>", views.user, name="user"),
    path("user/<int:user_id>/owned", views.owned, name="owned")
]
