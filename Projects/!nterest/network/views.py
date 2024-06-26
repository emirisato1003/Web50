from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.urls import reverse
# new import
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.http import JsonResponse

from .forms import ProfileForm, IconForm
from .models import User, Categories, Post, Follow, Profile, Like, Save


def index(request):
    all_post = Post.objects.all().order_by('date_posted').reverse()
    # for posts in all_post:
    #     print(posts)
    all_categories = Post.objects.all() 
    all_likes = Like.objects.all()
    user_liked = []
    try:
        for like in all_likes:
            if not request.user.id in user_liked:
                if like.user.id == request.user.id:
                    user_liked.append(like.post.id)
    except:
        user_liked = []

    return render(request, "network/index.html",{
        "all_post" : all_post,
        "all_categories": all_categories,
        "user_liked": user_liked
    })

def save(request, user_id):
    user = User.objects.get(pk=user_id)
    saved = Save.objects.all()
    for posts in saved:
        save_post = posts.post
    context = {
        'user': user,
        'save_post': save_post,
    }
    return render(request, "network/save.html", context)

@login_required(login_url='login')
def saved(request):
    user = request.user
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    # check if the post is already saved by the user
    save_filter = Save.objects.filter(post=post, user=user).first()
    if save_filter is None:
        new_save = Save.objects.create(post=post, user=user, is_save=True)
        new_save.save()
        return redirect('detail', post_id=post_id)
    else:
        save_filter.delete()
        return redirect('detail', post_id=post_id)


def create(request):
    if request.method == "GET":
        all_categories = Categories.objects.all()
        return render(request, "network/create.html",{
        "all_categories": all_categories
    })
    if request.method == "POST":
        file = request.FILES["img_file"]
        title = request.POST["title"]
        description = request.POST["description"]
        category_select = request.POST.get("category_select")
        category_input = request.POST.get("category_input")
        current_user = request.user        
        if category_input:
            new_category = Categories(category_name=category_input)
            new_category.save()
            new_post = Post(
            post=file,
            title=title,
            description=description,
            user=current_user,
            category=new_category
            )
            new_post.save()
        elif category_select:
            try:
                category_id = int(category_select)
                new_category = Categories.objects.get(id=category_id)
                new_post = Post(
                    post=file,
                    title=title,
                    description=description,
                    user=current_user,
                    category=new_category
                    )
                new_post.save()
                # select_category.save()
            except ValueError:
                pass
        
        messages.success(request, 'Your post has been created successfully!')
        # redirect the index page
        return HttpResponseRedirect(reverse("index"))
    

def detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    category = post.category
    saved = Save.objects.filter(post=post, user=request.user).first()
    categorized_post = Post.objects.filter(category=category)
    all_likes = Like.objects.all()
    user_liked = []
    try:
        for like in all_likes:
            if not request.user.id in user_liked:
                if like.user.id == request.user.id:
                    user_liked.append(like.post.id)
    except:
        user_liked = []
    return render(request, "network/detail.html",{
        "post": post,
        "categorized_post": categorized_post,
        "user_liked": user_liked,
        "saved": saved 
    })

def follow_user(request):
    follow_to_user = request.POST["following"]
    current_user = User.objects.get(pk=request.user.id)
    followed = User.objects.get(username=follow_to_user)
    f = Follow(user_following=current_user, follower=followed)
    f.save()
    follower_id = followed.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': follower_id}))

@login_required(login_url='login')
def liked(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    user = request.user

    like_filter = Like.objects.filter(post=post, user=user).first()

    if like_filter is None:
        new_like = Like.objects.create(post=post, user=user)
        like_count = post.post_like.count()
        new_like.save()
        return JsonResponse({'like_count': like_count, 'liked': True})
    else:
        like_filter.delete()
        like_count = post.post_like.count()
        # print(like_count)
        return JsonResponse({'like_count': like_count, 'liked': False})

def unfollow_user(request):
    follow_to_user = request.POST["unfollowing"]
    current_user = request.user
    followed = User.objects.get(username=follow_to_user)
    f = Follow.objects.get(user_following=current_user, follower=followed)
    f.delete()
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': followed.id}))

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

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    p_form = ProfileForm(request.POST or None, request.FILES or None)
    i_form = IconForm(request.POST or None, request.FILES or None)
    if Profile.objects.filter(user=user).exists():
        profile_img = Profile.objects.get(user=user)
    else:
        profile_img = None
    profile_user = User.objects.get(pk=user_id)
    if Post.objects.filter(user=profile_user).exists():
        all_user_posts = Post.objects.filter(user=profile_user).order_by('id').reverse()
        for posts in all_user_posts:
            users_post = posts
    else:
        all_user_posts = None
        users_post = None

    following = Follow.objects.filter(user_following=profile_user)
    follower = Follow.objects.filter(follower=profile_user)
    try:
        check_follow = follower.filter(user_following=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False

    all_likes = Like.objects.all()
    user_liked = []
    try:
        for like in all_likes:
            if not request.user.id in user_liked:
                if like.user.id == request.user.id:
                    user_liked.append(like.post.id)
    except:
        user_liked = []

    return render(request, "network/profile.html",{
        "profile_user":profile_user,
        "posts": all_user_posts,
        "following": following,
        "follower":follower,
        "isFollowing": isFollowing,
        "users_post": users_post,
        "profile_img": profile_img,
        "p_form": p_form,
        "i_form": i_form,
        "user_liked": user_liked
    })

def edit_profile(request, user_id):
    p_form = ProfileForm()
    i_form = IconForm()
    if request.method == "POST":
        # try:
        if Profile.objects.filter(user=user_id).exists():
            print('Profile exists')
            profile = Profile.objects.get(user=user_id)
            p_form = ProfileForm(request.POST, request.FILES, instance=profile)
            i_form = IconForm(request.POST, request.FILES, instance=profile)
        elif Profile.objects.filter(user=user_id).exists() == False:
            print('Profile does not exist')
            new_profile = Profile(user=User.objects.get(pk=user_id))
            new_profile.save()
            p_form = ProfileForm(request.POST, request.FILES, instance=new_profile)
            i_form = IconForm(request.POST, request.FILES, instance=new_profile)
        # try:
        #     profile = Profile.objects.get(pk=user_id)
        # except Profile.DoesNotExist:
        #     return JsonResponse({'error': 'Invalid profile ID'}, status=400)

        # p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        # i_form = IconForm(request.POST, request.FILES, instance=profile)

        if p_form.is_valid() and i_form.is_valid():
            print(p_form, i_form)
            p_form.save()
            i_form.save()
            return JsonResponse({'success': True})
        else:
            errors = {}
            if not p_form.is_valid():
                errors['profile_form'] = p_form.errors
            if not i_form.is_valid():
                errors['icon_form'] = i_form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)

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
