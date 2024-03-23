from django.contrib import admin
from .models import Auction_Listing, Bid, Category, Comment, Watchlist

from .models import User


class Auction_Listing_Admin(admin.ModelAdmin):
    list_display = ("id", "status", "item", "price", "date_created", "user", "category")

class Bid_Admin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "price", "date_created")


class Category_Admin(admin.ModelAdmin):
    list_display = ("id", "name")


class Comment_Admin(admin.ModelAdmin):
    list_display = ("id","date_created", "user_id", "comment")


class User_Admin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")
    
    
class Watchlist_Admin(admin.ModelAdmin):
    list_display = ("id", "user_id", "listing_id", "date_created")


admin.site.register(Auction_Listing, Auction_Listing_Admin)
admin.site.register(Bid, Bid_Admin)
admin.site.register(Category, Category_Admin)
admin.site.register(Comment, Comment_Admin)
admin.site.register(User, User_Admin)
admin.site.register(Watchlist, Watchlist_Admin)


