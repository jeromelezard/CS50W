from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

class NewPost(forms.Form):
    post_content = forms.CharField(label="", required=True, widget=forms.Textarea(attrs={'class' : 'postContent', 'autocomplete' : 'off', 'placeholder' : 'Make a new post...'}))

class ContactListView(ListView):
    paginate_by = 2
    model = Post
    
@csrf_exempt
def index(request):
    form = NewPost(request.POST)
    if request.method == "POST":
        if form.is_valid():
            content = form.cleaned_data["post_content"]
            newPost = Post(content=content, user=request.user)
            newPost.save()
            return HttpResponseRedirect(reverse('index'))
    
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "form": NewPost(),
        "posts": posts,
        "index": True,
        'page_obj': page_obj 
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
            newFollow = Following(from_user=user)
            user.save()
            newFollow.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def like(request):
    if request.method != "POST":
        return JsonResponse({'error': 'POST required'}, status=400)
    data = json.loads(request.body)
    try:
        post = Post.objects.get(pk=data.get("post_id"))
    except:
        return JsonResponse({'error': 'Post not found'}, status=404)
    
    if request.user.id is None:
        return JsonResponse({'likes': None, 'error': 1})
    user = request.user
    
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    
    return JsonResponse({'likes': post.likes.count(), 'error': None})


@csrf_exempt
@login_required
def saveEdit(request):
    
    if request.method != "POST":
        return JsonResponse({'error': 'POST required'}, status=400)
    data = json.loads(request.body)
    postData = Post.objects.get(pk=data.get("post_id"))
    if postData.user.id != request.user.id: 
        return JsonResponse({'error': 'Incorrect user'}, status=400)
    if len(str(data.get("new_post"))) - str(data.get("new_post")).count(" ") == 0:
        return JsonResponse({'error': 'Empty string'}, status=400)
    postData.content = str(data.get("new_post"))
    postData.save()
    return JsonResponse({'new_content': Post.objects.get(pk=data.get("post_id")).content})


def profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(user=user).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    following = Following.objects.get(from_user=request.user)
    userFollowing = Following.objects.get(from_user=user)
    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        "following": following,
        "userFollowing": userFollowing,
        'page_obj': page_obj
    })
@csrf_exempt
def follow(request):
    if request.method != "POST":
        return JsonResponse({'error': 'post required'}, status=405)
    data = json.loads(request.body)
    profile = User.objects.get(pk=data.get("user"))

    user = request.user
    
    newFollow = Following.objects.get(from_user=user)
    if profile in newFollow.following.all():
        newFollow.following.remove(profile)
        #remove user into profiles following info
        removeFollower = Following.objects.get(from_user=profile)
        removeFollower.followers.remove(user)
        return JsonResponse({'message': 'Follow', 'count': removeFollower.followers.count()})
    else:
        newFollow.following.add(profile)
        #add user into profiles following info
        addFollower = Following.objects.get(from_user=profile)
        addFollower.followers.add(user)
        return JsonResponse({'message': 'Unfollow', 'count': addFollower.followers.count()}) 
    

@login_required
def following(request):
    following = Following.objects.get(from_user=request.user).following.all()

    posts = Post.objects.filter(user__in=following).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        
        "page_obj": page_obj,
        "index": False
    })

@login_required
def userFollowing(request, id):
    user = User.objects.get(pk=id)
    return render(request, "network/users.html", {
        "users": Following.objects.get(from_user=user).following.all()
    })

@login_required
def userFollowers(request, id):
    user = User.objects.get(pk=id)
    return render(request, "network/users.html", {
        "users": Following.objects.get(from_user=user).followers.all()
    })  