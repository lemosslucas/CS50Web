from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
import json 

from .models import User, Post, Follow, Like


def index(request):
    posts = Post.objects.all().order_by("date").reverse()

    paginator = Paginator(posts, 10)
    number_page = request.GET.get("page")
    posts_in_the_page = paginator.get_page(number_page)

    likes = Like.objects.all()
    posts_liked = []

    for like in likes:
        if like.user == request.user:
            posts_liked.append(like.post.id)

    return render(request, "network/index.html", {
        "posts": posts, 
        "posts_in_the_page": posts_in_the_page,
        "posts_liked": posts_liked,
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def add_new_post(request):
    if request.method == "POST":
        user = request.user
        text = request.POST['text']
        
        new_post = Post(
            user = user,
            text = text
        )

        new_post.save()
        return HttpResponseRedirect(reverse("index"))

def load_user_page(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by("date").reverse()

    paginator = Paginator(posts, 10)
    number_page = request.GET.get("page")
    posts_in_the_page = paginator.get_page(number_page)

    followed = Follow.objects.filter(followed=user)
    follower = Follow.objects.filter(follower=user)
    is_follow = Follow.objects.filter(follower=request.user, followed=user).exists()

    likes = Like.objects.all()
    posts_liked = []

    for like in likes:
        if like.user == request.user:
            posts_liked.append(like.post.id)

    return render(request, "network/user_page.html", {
        "posts": posts, 
        "posts_in_the_page": posts_in_the_page,
        "username": user.username,
        "followed": followed,
        "follower": follower,
        "is_follow": is_follow,
        "actual_user": request.user.username,
        "user_id": user_id,
        "posts_liked": posts_liked
    })

def follow(request, user_id):
    print(user_id)
    print(request.user)
    followed = User.objects.get(pk=user_id)
    print(followed.id)

    new_follower = Follow(
        follower = request.user,
        followed = followed
    )
    new_follower.save()
   
    return HttpResponseRedirect(reverse('load_user_page', kwargs={'user_id':user_id}))

def unfollow(request, user_id):
    print(user_id)
    print(request.user)
    followed = User.objects.get(pk=user_id)
    print(followed)
    
    try:
        follow = Follow.objects.get(follower=request.user, followed=followed)
        follow.delete()  
    except Follow.DoesNotExist:
        pass
   
    return HttpResponseRedirect(reverse('load_user_page', kwargs={'user_id':user_id}))

def edit_post(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        edit_post = Post.objects.get(pk=post_id)
        edit_post.text = text
        edit_post.save()

        return JsonResponse({"text": text})
    
@login_required
def following_page(request):
    actual_user = User.objects.get(pk=request.user.id)
    followings = Follow.objects.filter(follower=actual_user)
    posts = Post.objects.all().order_by('date').reverse()

    posts_followings = []

    for post in posts:
        #print(post)
        for following in followings:
            if following.followed == post.user:
                posts_followings.append(post)

    paginator = Paginator(posts_followings, 10)
    number_page = request.GET.get("page")
    posts_in_the_page = paginator.get_page(number_page)

    likes = Like.objects.all()
    posts_liked = []

    for like in likes:
        if like.user == request.user:
            posts_liked.append(like.post.id)

    return render(request, "network/index.html", {
        "posts":posts, 
        "posts_in_the_page": posts_in_the_page,
        "posts_liked": posts_liked,
    })

@login_required
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user 
    like = Like(user=user, post=post)
    like.save()

    likes_count = Like.objects.filter(post=post).count()
    return JsonResponse({"message":"Liked", 'likes_count':likes_count})

@login_required
def unlike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user 
    unlike = Like.objects.filter(user=user, post=post)
    unlike.delete()

    likes_count = Like.objects.filter(post=post).count()
    return JsonResponse({"message":"Unliked", 'likes_count':likes_count})