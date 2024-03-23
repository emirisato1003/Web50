from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name

class Bit(models.Model):
    bit_user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, related_name="bit_user")
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Listings(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    bit = models.ForeignKey(Bit, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    imageUrl = models.CharField(max_length=1000, null=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.title

class Watchlists(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, related_name="user_name")
    listing_title = models.ForeignKey(Listings,on_delete=models.CASCADE,blank=True, related_name="listing_title")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_listing")
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.comment


