from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

    
class Auction_Listing(models.Model):
    item = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    img = models.CharField(max_length=256,null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    date_created = models.DateTimeField(auto_now_add=True)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    winner = models.CharField(max_length=64, null=True, blank=True)
    status = models.BooleanField(default=True)
    bid_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.item}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="bid_listing")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user} Listing: {self.listing} Price: {self.price} Date: {self.date_created}"
    
class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing_id = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="comment_listing")
    comment = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"User: {self.user_id} Listing ID: {self.listing_id} Comment: {self.comment}"


class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing_id = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="watchlist_listing")
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}"