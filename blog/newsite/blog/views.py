from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import BlogPost
from django.contrib.auth.models import User
from django.db import DatabaseError

# authentication
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import re
from django.contrib.auth.hashers import make_password

# rework to be home page

# homepage


def homepage(request):
    latest_blog_list = BlogPost.objects.order_by('-date_created')
    context = {'latest_blog_list': latest_blog_list}
    return render(request, 'blog/homepage.html', context)


def details(request, blog_id):
    # try except
    try:
        blog = BlogPost.objects.get(pk=blog_id)
    except BlogPost.DoesNotExist:
        raise Http404("Blog Does Not Exist")
    return render(request, 'blog/details.html', {"blog": blog})

# register


def register_user(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('blog:signup')

        # Check if username is already taken
        if User.objects.filter(username=user_name).exists():
            messages.error(request, "Username already taken!")
            return redirect('blog:signup')

        # storing in db
        # try using the built-in django user model and use the create_user function to hash the plain password
        user = User.objects.create_user(
            username=user_name,  # 'username' is the default field for username in Django's User model
            email=email,
            password=password,   # Raw password; Django hashes it internally
            # work on it later
        )

        messages.success(request, "Accounted created successfully")
        return redirect('blog:login')
    # always return an http response
    return render(request, 'blog/signup.html')
    # get 2 passwords from the user and compare before storing one in encrypted form

# django has a built-in login so dont define login on your own


def login_user(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        print(f"{user_name} and {password}")

        # Authenticate the user against the db
        user = authenticate(request, username=user_name, password=password)

        if user is not None:
            # if the user is found the credentials match
            login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('blog:homepage')
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'blog/login.html')


def create_blog(request):
    if request.method == "POST":
        author = request.user
        title = request.POST.get('title')
        detail = request.POST.get('details')

        try:
            blogpost = BlogPost.objects.create(
                author=author,
                title=title,
                details=detail
            )
            messages.success(request, "Blog Post was created successfully")
            return redirect('blog:homepage')
        except DatabaseError as e:
            # Handle any database-related errors
            messages.error(
                request, f"An error occurred while saving the blog post: {e}")
        except Exception as e:
            # Catch any other general exceptions
            messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'blog/new_blog.html')


def update(request):
    pass


def delete_post(request):
    pass
