from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .forms import NewUserForm


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


def homepage(request):
    return HttpResponse("Home Page Working")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/api/v1/posts/")
        else:
            messages.error(request, "Unsuccessful registration.")
    else:
        form = NewUserForm()

    return render(request, "blog/register.html", {"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect("/api/v1/posts/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "blog/login.html", {"login_form": form})


def logout_request(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("/api/v1/login/")