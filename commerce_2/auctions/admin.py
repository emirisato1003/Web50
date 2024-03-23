from django.contrib import admin

# new import
from .models import User, Categories, Listings, Watchlists, Comment, Bid

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid_price", "bid_user")

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "owner","date_created")

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

class WatchlistsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing_title")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "comment")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Watchlists, WatchlistsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)


