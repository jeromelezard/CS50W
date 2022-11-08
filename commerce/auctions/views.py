from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Listing, Bid, Comments, Watchlist, Categories
from django.db.models import Max
from .forms import *

def index(request):
    listings = Listing.objects.all().order_by('-date_created')
    return render(request, "auctions/index.html", {
        "listings": listings,
        "page_title": "Active Listings",
        "index": True
    })

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

        if not username:
            return render(request, "auctions/register.html", {
                "message": "Please provide username."
            })
        if not password:
            return render(request, "auctions/register.html", {
                "message": "Please provide password."
            })
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


@login_required
def create_listing(request):
    form = NewListingForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            if not description: description = None 
            price = form.cleaned_data["starting_price"]
            url = form.cleaned_data["image_url"]
            if not url: url = None 
            category_name = form.cleaned_data["category"]
            if category_name: 
                category = Categories.objects.get(category=category_name)
            else:
                category = None
            
            new_listing = Listing(title=title, description=description, starting_price=price, url=url, category=category, listed_by=request.user)
            new_listing.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id' : new_listing.id}))
    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })

def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category = Categories.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category).order_by('-date_created')
    return render(request, "auctions/index.html", {
        "listings": listings,
        "page_title": category,
        "category": True
    })
    

def listing(request, listing_id):
    # get info about current listing
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/notFound.html")
   
    # find the highest bid
    bids = Bid.objects.filter(listing_id=listing_id)
    
    length = len(bids)
    if length > 0:
        max = "{:.2f}".format(bids.aggregate(Max('bid_amount'))["bid_amount__max"])
    else:
        max = None
    try:
        comments = Comments.objects.filter(listing=listing).order_by('-date')
    except Comments.DoesNotExist:
        comments = None
    form = NewBidForm(request.POST)
    commentForm = MakeComment(request.POST)
    
    error = []
    if request.method == "POST":
        if 'bid_amount' in request.POST:
            if form.is_valid():
                if listing.active == True:
                    bid_amount = float(form.cleaned_data["bid_amount"])
                    current_bids = Bid.objects.filter(listing_id=listing_id)
                    if len(current_bids) > 0:
                        max_bid = float(bids.aggregate(Max('bid_amount'))["bid_amount__max"])
                        if bid_amount > max_bid:
                            new_bid = Bid(listing=listing, bid_amount=bid_amount, user=request.user)
                            new_bid.save()
                            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id' : listing.id}))
                        else:
                            error.clear()
                            error.append("Bid must be larger than largest bid")
                    if len(current_bids) == 0:
                        if bid_amount > float(listing.starting_price):
                            new_bid = Bid(listing=listing, bid_amount=bid_amount, user=request.user)
                            new_bid.save()
                            return HttpResponseRedirect(reverse('listing', kwargs={'listing_id' : listing.id}))
                        else:
                            error.clear()
                            error.append("Bid must be larger than starting price")
            else:
                error.clear()
                error.append("Number too large") 
                
        if 'close_listing' in request.POST:
            current_bids = len(Bid.objects.filter(listing_id=listing_id))
            if current_bids == 0:
                listing.owner = None
                listing.active = False
                listing.save()
                return HttpResponseRedirect(reverse('index'))

            else:
                max_bid = "{:.2f}".format(bids.aggregate(Max('bid_amount'))["bid_amount__max"])
                winner = bids.filter(bid_amount=max_bid)
                listing.owner = winner[0].user
                listing.active = False  
                listing.save()
                return HttpResponseRedirect(reverse('listing', kwargs={'listing_id' : listing.id}))
        if 'watchlist' in request.POST:
            add = Watchlist(user=request.user, listing=listing)
            add.save()
        if 'remove' in request.POST:
            remove = Watchlist.objects.get(user=request.user, listing=listing)
            remove.delete()
        if 'is_comment' in request.POST:
            if commentForm.is_valid():
                comment = commentForm.cleaned_data["comment"]
                new_comment = Comments(user=request.user, listing=listing, comment=comment)
                new_comment.save()
                return HttpResponseRedirect(reverse('listing', kwargs={'listing_id' : listing.id}))

    try:
        Watchlist.objects.get(user=request.user, listing=listing)
        watched = True
    except:
        watched = False
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bidForm": NewBidForm(),
        "closeForm": CloseListing(),
        "watchForm": AddToWatchlist(),
        "removeForm": RemoveFromWatchlist(),
        "commentForm": MakeComment(),
        "length": length,
        "error": error,
        "max": max,
        "watched": watched,
        "comments": comments
    })

def watchlist(request):
    listings = []
    items = Watchlist.objects.filter(user=request.user)
    for i in range(len(items)):
        listings.append(items[i].listing)
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "page_title": "My Watchlist",
        "watchlist": True
    })

@login_required
def user(request, user_id):
    user = User.objects.get(pk=user_id)
    listings = Listing.objects.filter(listed_by=user)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "profile": True,
        "my_listings": True,
        "userPage": user
    })

@login_required
def owned(request, user_id):
    user = User.objects.get(pk=user_id)
    listings = Listing.objects.filter(owner=user)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "profile": True,
        "my_owned": True,
        "userPage": user
    })
