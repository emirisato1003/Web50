from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Auction_Listing, Bid, Category, User, Comment, Watchlist

from .models import User

@login_required(login_url='login')
def bid(request):
    if request.method == "POST": 
        user_id = request.user.id
        user = User(id=user_id)
        bid = request.POST["bid"]
        listing_id = request.POST["listing_id"]
        listing = Auction_Listing.objects.get(id=listing_id)
        listing.bid_count = listing.bid_count + 1
        listing.current_bid = float(bid)
        listing.save()
        
        highest_bid = Bid.objects.filter(listing_id=listing_id).order_by("-price").first()
        
        if highest_bid is None:
            highest_bid = listing.price
        else:
            highest_bid = highest_bid.price
                
        if float(bid) > highest_bid:
            bid = Bid(user=user, listing=listing, price=bid)
            bid.save()
            watching = Watchlist.objects.filter(user_id=request.user.id, listing_id=listing)
            messages.info(request,"✅ Your bid was successfully received.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
        else:
            watching = Watchlist.objects.filter(user_id=request.user.id, listing_id=listing)

            if not watching:
                watching = False
            else:
                watching = watching.first()
                watching = watching.id

            messages.info(request,"🛑 Your bid must be higher than the current bid amount.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))    
        
        
@login_required(login_url='login')
def get_watching(request):
    watching = Watchlist.objects.filter(user_id=request.user.id)
    return len(watching)


@login_required(login_url='login')
def add_comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        listing = Auction_Listing.objects.get(id=listing_id)
        comment = Comment(user_id=user, listing_id=listing, comment=comment)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return render(request, "auctions/listing.html",{
            "message": "There was an error adding your comment. Please try again."
        })


def categories(request):
    count = get_watching(request)
    categories = Category.objects.order_by("name")
    return render(request, "auctions/categories.html",{"categories": categories, "count": count})


def category(request, category):
    count = get_watching(request)
    id = Category.objects.get(name=category).id
    listings = Auction_Listing.objects.filter(category=id)
    return render(request, "auctions/category.html",{"category": category, "listings": listings, "count": count})


def index(request):
    count = get_watching(request)
    listings = Auction_Listing.objects.filter(status=True).order_by("-date_created")
    return render(request, "auctions/index.html",{"listings": listings, "count": count})


@login_required(login_url='login')
def close(request,listing_id):
    listing = Auction_Listing.objects.get(id=listing_id)
    listing.status = False
    # get the user with the highest bid
    winning_bid = Bid.objects.filter(listing_id=listing_id).order_by("-price").first()
    listing.winner = winning_bid.user.username
    listing.save()
    return HttpResponseRedirect(reverse("closed"))
    

def closed(request):
    count = get_watching(request)
    listings = Auction_Listing.objects.filter(status=False)
    return render(request, "auctions/closed.html",{"listings": listings, "count": count})


@login_required(login_url='login')
def create(request):
    count = get_watching(request)
    if request.method == "POST":
        item = request.POST["item"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        image = request.POST["img"]
        user = request.user
        category = Category.objects.get(name=category)
        listing = Auction_Listing(item=item, description=description, price=price, category=category, img=image, user=user)
        listing.save()
        message = f"Your <strong>{item}</strong> listing was successfully created. Good luck! 🍀"
        return HttpResponseRedirect(reverse("index") + "?message=" + message)
    else:
        return render(request, "auctions/create.html",{"count": count})


@login_required(login_url='login')
def edit(request, listing_id):
    count = get_watching(request)
    listing = Auction_Listing.objects.get(id=listing_id)
    return render(request, "auctions/edit.html",{"listing": listing, "count": count})


@login_required(login_url='login')
def edit_save(request, listing_id):
    if request.method == "POST":
        item = request.POST["item"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        image = request.POST["img"]
        category = Category.objects.get(name=category)
        listing = Auction_Listing.objects.get(id=listing_id)
        listing.item = item
        listing.description = description
        listing.price = price
        listing.category = category
        listing.img = image
        listing.save()
        message = f"Your <strong>{item}</strong> listing was successfully updated. Good luck! 🍀"
        return HttpResponseRedirect(reverse("index") + "?message=" + message)


def listing(request, listing_id):
    count = get_watching(request)
    listing = Auction_Listing.objects.get(id=int(listing_id))
    comments = Comment.objects.filter(listing_id=listing_id)
    bids = Bid.objects.filter(listing_id=listing_id)
    highest_bidder = Bid.objects.filter(listing_id=listing_id).order_by("-price").first()
    
    if request.user:
        is_watching = Watchlist.objects.filter(user_id=request.user.id, listing_id=listing)
        if len(is_watching) == 0:
            is_watching = None
        else:
            is_watching = is_watching.first()
            is_watching = is_watching.id
        
    return render(request, "auctions/listing.html",{"listing": listing,"comments": comments, "watching": is_watching, "count": count, "bids": bids, "highest_bidder": highest_bidder})


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
                "message": "Invalid username and/or password. Please try again."
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


@login_required(login_url='login')   
def watch(request, listing_id):
    if request.method == "POST":
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        listing = Auction_Listing.objects.get(id=listing_id)
        entry = Watchlist(user_id=user, listing_id=listing)
        entry.save()
        # count = get_watching(request)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return render(request, "auctions/listing.html",{
            "message": "Error adding to watchlist"
        })


@login_required(login_url='login')
def watch_remove(request,listing_id):
    if request.method == "POST":
        try:
            redirect = request.GET["redirect"]
            id = request.POST["listing"]
        except:
            redirect = False
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        entry = Watchlist.objects.get(user_id=user, id=listing_id,)
        # Delete entry  
        entry.delete()
        if redirect != "listing":
            return HttpResponseRedirect(reverse("watchlist"))
        else:
            return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        return render(request, "auctions/listing.html",{
            "message": "Error removing from watchlist"
        })


@login_required(login_url='login')
def watchlist(request):
    watching = Watchlist.objects.filter(user_id=request.user.id)
    count = get_watching(request)
    return render(request, "auctions/watchlist.html",{"watching": watching, "count": count})