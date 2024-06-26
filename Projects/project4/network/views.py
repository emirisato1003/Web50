import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import User, Posts, Follow, Like, Comment

@login_required
def add_like(request, post_id):
    post = Posts.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    new_like = Like(user_like=user, post=post, is_liked=True)
    new_like.save()
    like_count = post.post_like.filter(is_liked=True).count()
    return JsonResponse({'like_count': like_count, "message": "Like added!"})

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Posts.objects.get(pk=post_id)
        edit_post.post = data["post"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["post"]})
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

def comment(request, post_id):
    user = User.objects.get(pk=request.user.id)
    post = Posts.objects.get(pk=post_id)
    if request.method == "POST":
        message = request.POST.get("comment")
        if message:
            comment = Comment(
                user=user,
                post= post,
                comment=message
            )
            comment.save()
            return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse('index'))


def index(request):
    all_posts = Posts.objects.all().order_by('id').reverse()
    all_comments = Comment.objects.all()
    for comments in all_comments:
        post_comments = comments
        post_id_comments = comments.post.id
        
    # create a Paginator object
    paginator = Paginator(all_posts,10)
    # retrieves the current page number from URL
    page_num = request.GET.get('page')
    current_page = paginator.get_page(page_num)
    all_likes = Like.objects.all()
    user_liked = []
    try:
        for like in all_likes:
            if not request.user.id in user_liked:
                if like.user_like.id == request.user.id:
                    user_liked.append(like.post.id)
    except:
        user_liked = [] 
    return render(request, "network/index.html",{
        "all_posts" : all_posts,
        "current_page": current_page,
        "user_liked" : user_liked,
        "message": "Log in or register to like this post",
        "post_comments": post_comments,
        "all_comments": all_comments
    })

def new_post(request):
    if request.method == "POST":
        new_post = request.POST["post"]
        post_user = User.objects.get(pk=request.user.id)
        # create a post object
        save_post = Posts(post=new_post, user=post_user)
        save_post.save()
        return HttpResponseRedirect(reverse("index"))

def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    all_user_posts = Posts.objects.filter(user=profile_user).order_by('id').reverse()

    following = Follow.objects.filter(user_following=profile_user)
    followers = Follow.objects.filter(follower=profile_user)

    try: 
        check_follow = followers.filter(user_following=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    return render(request, "network/profile.html",{
        "all_user_posts" : all_user_posts,
        "username": profile_user.username,
        "profile_user" : profile_user,
        "following": following,
        "follower": followers,
        "isFollowing": isFollowing,
    })

@login_required
def remove_like(request, post_id):
    post = Posts.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter(user_like=user, post=post)
    like.delete()
    like_remove_count = post.post_like.filter(is_liked=True).count()
    return JsonResponse({'like_remove_count': like_remove_count, "message": "Like removed!"})

def follow(request):
    new_user_follow = request.POST["user_following"]
    current_user_id = User.objects.get(pk=request.user.id)
    followed_user = User.objects.get(username=new_user_follow)
    f = Follow(user_following=current_user_id, follower=followed_user)
    f.save()
    follower_id = followed_user.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': follower_id}))


def unfollow(request):
    new_user_follow = request.POST["user_unfollowing"]
    current_user_id = User.objects.get(pk=request.user.id)
    followed_user = User.objects.get(username=new_user_follow)
    f = Follow.objects.get(user_following=current_user_id, follower=followed_user)
    f.delete()
    follower_id = followed_user.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': follower_id}))

@login_required
def following(request, user_id):
    if request.method == "GET":
        current_user = User.objects.get(pk=request.user.id)
        following_user = Follow.objects.filter(user_following=current_user)
        all_posts = Posts.objects.all().order_by('id').reverse()

        following_user_posts = []

        for posts in all_posts:
            for user in following_user:
                if user.follower == posts.user:
                    following_user_posts.append(posts)

        # create a Paginator object
        paginator = Paginator(following_user_posts,10)
        # retrieves the current page number from URL
        page_num = request.GET.get('page')
        current_page = paginator.get_page(page_num)
        return render(request, "network/following.html",{
            "current_page": current_page,
        })
    else:
        return render(request, "network/login.html")

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
