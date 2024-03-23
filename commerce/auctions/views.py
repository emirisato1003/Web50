from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# mew import
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Category, Listings, Comment, Bit

def index(request):
    if request.method == "GET":
        active_listings = Listings.objects.all()
        return render(request, "auctions/index.html",{
            "auction_listings" : active_listings,
            "categories" : Category.objects.all()
        })
    if request.method == "POST":
        categoryFromForm = request.POST["category"]
        get_category = Category.objects.get(id=categoryFromForm)
        auction_listings = Listings.objects.filter(category=get_category)
        print(auction_listings)
        return render(request, "auctions/index.html",{
                "auction_listings" : auction_listings,
                "categories" : Category.objects.all()
            })   

# Bit function 

# comment function
def comment(request, listing_id):
    user = request.user
    listings = Listings.objects.get(id=listing_id)
    if request.method == "POST":
        message = request.POST["comment"]
        comment = Comment(
            user=user, 
            listing=listings, 
            comment=message
        )
        comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )),{
        "message" : "successful"
    })

# create function
@login_required
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html",{
            "categories": Category.objects.all()
            })
            
    if request.method == "POST":
        print("posting...")
        #get each data from form
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        imageUrl = request.POST["imageUrl"]
        category = request.POST["category"]

        print(price)
        # define the user
        current_user = request.user
        #insert the object in our database
        category = Category.objects.get(id=category)
        # create a bit
        bit = Bit(bit_user=current_user, price=float(price))
        bid.save()
        listing = Listings(
            title=title, 
            description=description, 
            bit=bit,
            category=category,
            imageUrl=imageUrl,
            owner=current_user
            )
        listing.save()
        # redirect the index page
        return HttpResponseRedirect(reverse("index"))
    

# listing function
def listing(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    is_listing_watchinglist = request.user in listing.watchlist.all()
    allComments = Comment.objects.filter(listing=listing)
    print(allComments)
    return render(request, "auctions/listing.html",{
        "listing" : listing,
        "is_listing_watchinglist": is_listing_watchinglist,
        "comment" : allComments
    })

# display watch list
def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html",{
        "auction_listings" : listings
    })

@login_required
# watchlist function
def removeWatchlist(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    currentUser = request.user
    listing.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

@login_required
def addWatchlist(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    currentUser = request.user
    listing.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
