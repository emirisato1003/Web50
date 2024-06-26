
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create,name="create"),
    path("detail/<int:post_id>", views.detail, name="detail"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow_user", views.follow_user, name="follow_user"),
    path("unfollow_user", views.unfollow_user, name="unfollow_user"),
    path("edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"),
    path("liked", views.liked, name="liked"),
    path("saved", views.saved, name="saved"),
    path("save/<int:user_id>", views.save, name="save"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)