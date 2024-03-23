from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Categories(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Bid(models.Model):
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="bid_user")


class Listings(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    imageUrl = models.CharField(max_length=1000, null=True)
    is_active = models.BooleanField(default=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")
    bid_count = models.IntegerField(default=0)

    def __str__(self):
        return f"title: {self.title} Price: {self.price.bid_price}"


class Watchlists(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, related_name="user_name")
    listing_title = models.ForeignKey(Listings,on_delete=models.CASCADE,blank=True, related_name="listing_title")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_listing")
    comment = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


