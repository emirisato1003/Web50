from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("removeWatchlist/<int:listing_id>",views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:listing_id>",views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("closed", views.closed, name="closed")
]
