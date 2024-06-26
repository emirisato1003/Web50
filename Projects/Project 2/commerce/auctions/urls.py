from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bid", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("closed", views.closed, name="closed"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("watch/<int:listing_id>", views.watch, name="watch"),
    path("watch_remove/<int:listing_id>", views.watch_remove, name="watch_remove"),
    path("edit/<int:listing_id>", views.edit, name="edit"),
    path("save/<int:listing_id>", views.edit_save, name="edit_save"),
]
