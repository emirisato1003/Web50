from django.contrib import admin

from .models import User, Categories, Post, Profile, Follow, Like, Save

# Register your models here.

# just created new models (Profile and Follow) and have to register new models here!

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "title", "date_posted", "description", "category", "user", "like")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "icon_img", "profile_img", "user")

class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "user_following", "follower")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "is_like")

class SaveAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "is_save")


admin.site.register(User, UserAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Save, SaveAdmin)