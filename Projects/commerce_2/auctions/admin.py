from django.contrib import admin

# new import
from .models import User, Category, Listings, Watchlists, Comment, Bit

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "owner")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

class WatchlistsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing_title")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "comment")

class BitAdmin(admin.ModelAdmin):
    list_display = ("id", "bit_user", "bit_price")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Watchlists, WatchlistsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bit, BitAdmin)


