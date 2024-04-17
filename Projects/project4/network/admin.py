from django.contrib import admin

from .models import User, Follow, Posts, Like, Dislike


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")

class PostsAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "date_posted")

class FollowAdmin(admin.ModelAdmin):
    list_display = ("user_following", "follower")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("user_like", "post")

class DislikeAdmin(admin.ModelAdmin):
    list_display = ("user_dislike", "post_dislike")

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)




