from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# mew import
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Categories, Listings, Comment, Bid, Watchlists

@login_required(login_url='login')
def get_watching(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return len(listings)
    

def index(request):
    if request.method == "GET":
        count = get_watching(request)
        print(get_watching(request))
        active_listings = Listings.objects.all()
        return render(request, "auctions/index.html",{
            "auction_listings" : active_listings,
            "categories" : Categories.objects.all(),
            "count" : count
        })
    if request.method == "POST":
        categoryFromForm = request.POST["category"]
        get_category = Categories.objects.get(id=categoryFromForm)
        auction_listings = Listings.objects.filter(category=get_category)
        return render(request, "auctions/index.html",{
                "auction_listings" : auction_listings,
                "categories" : Categories.objects.all()
            })   

# Bid function 
@login_required(login_url='login')
def bid(request, listing_id):
    biding_price = request.POST["bid"]
    listing = Listings.objects.get(id=listing_id)
    if float(biding_price) > listing.price.bid_price:
        new_bid = Bid(bid_price=biding_price, bid_user=request.user)
        new_bid.save()
        listing.price = new_bid
        listing.bid_count = listing.bid_count + 1 # =+ ?
        listing.save()
        return render(request, "auctions/listing.html",{
            "listing" : listing,
            "message": "Bid was updated successfully",
            "update": True
        })
    else:
        return render(request, "auctions/listing.html",{
            "listing" : listing,
            "error_message": "The Bid price must be higher than current price",
            "update": False
        })


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
@login_required(login_url='login')
def create(request):
    if request.method == "GET":
        currentUser = request.user
        listings = currentUser.listingWatchlist.all()
        count = len(listings)
        return render(request, "auctions/create.html",{
            "categories": Categories.objects.all(),
            "count": count
            })
            
    if request.method == "POST":
        #get each data from form
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        imageUrl = request.POST["imageUrl"]
        category = request.POST["category"]
        # define the user
        current_user = request.user
        #insert the object in our database
        category = Categories.objects.get(id=category)
        # create a bit
        bid = Bid(bid_price=price, bid_user=current_user)
        bid.save()
        # create a new listing object
        listing = Listings(
            title=title, 
            description=description, 
            price=bid,
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
    return render(request, "auctions/listing.html",{
        "listing" : listing,
        "is_listing_watchinglist": is_listing_watchinglist,
        "comment" : allComments,
        "categories": Categories.objects.all()
    })

@login_required(login_url='login')
def close(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))


def closed(request):
    if request.method == "GET":
        currentUser = request.user
        listings = currentUser.listingWatchlist.all()
        count = len(listings)
        listing = Listings.objects.filter(is_active=False)
        return render(request, "auctions/closed.html",{
            "closed_listings" : listing,
            "count" : count
        })

# display watch list
@login_required(login_url='login')
def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    count = len(listings)
    return render(request, "auctions/watchlist.html",{
        "auction_listings" : listings,
        "count" : count
    })

@login_required(login_url='login')
def count_watchlist(request):
    current_user = request.user
    listings = current_user.listingWatchlist.all()
    count = len(listings)
    return render(request, "auctions/layout.html",{
        "count": count
    })

# watchlist function
@login_required(login_url='login')
def removeWatchlist(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    currentUser = request.user
    listing.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

@login_required(login_url='login')
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
