from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        'listings': listings
    })

def listing(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    comments = Comment.objects.filter(listing=listing_id)

    user_current = request.user
    is_listing_in_watchlist = user_current in listing.watchlist.all()

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'comments': comments,
        "is_listing_in_watchlist": is_listing_in_watchlist
    })

def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.closed = True
    listing.save()

    return HttpResponseRedirect(reverse('listing', args=(listing_id, )))

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

def create_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else :
        if request.method == 'POST':
            title = request.POST.get('title')
            url_img = request.POST.get('url_img', '')
            category = request.POST.get('category')
            description = request.POST.get('description')
            
            bid = Bid(new_bid_offer=float(request.POST['bid']), user=request.user)
            bid.save()

            new_item = Listing (
                title=title,
                description=description,
                user_own=request.user,
                bid=bid,
                category=category,
                url_img=url_img,
                closed=False
            )
            new_item.save()

            return render(request, "auctions/index.html", {
                'message': 'Your item has been posted!'
            })
        
    return render(request, 'auctions/create.html')

def new_bid(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    new_bid_offer = float(request.POST.get('new_bid_offer'))

    if listing.bid.new_bid_offer < new_bid_offer:
        listing.bid.new_bid_offer = new_bid_offer
        listing.save()
        
        new_bid = Bid(
            new_bid_offer = new_bid_offer, 
            user = request.user
        )
        
        new_bid.save()
        listing.bid = new_bid

        listing.save()
        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'message': 'Your bid is the current bid!'
        })
    
    return render(request, 'auctions/listing.html',{
            'listing': listing,
            'message': 'Erro! Your bid is smallest then current bid!'
    })

def listing_watchlist(request):
    user_current = request.user
    listings = user_current.watch_listings.all()

    return render(request, 'auctions/watchlist.html', {
        'listings': listings
    })

def add_watchlist(request, listing_id):
    user_current = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.add(user_current)

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def remove_watchlist(request, listing_id):
    user_current = request.user
    listing = Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(user_current)

    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def listing_categories(request):
    categories= Listing.objects.values_list('category', flat=True).distinct()

    return render(request, 'auctions/categories.html', {
        'categories':categories
    })

def index_filter(request, category):
    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/indexfilter.html", {
        'listings': listings
    })

def add_comment(request, listing_id):
    user_current = request.user
    listing = Listing.objects.get(pk=listing_id)
    text = request.POST.get('comment')

    new_comment = Comment(text=text, user=user_current, listing=listing)
    new_comment.save()

    return HttpResponseRedirect(reverse('listing', args=(listing_id, )))