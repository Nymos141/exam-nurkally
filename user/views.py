from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View

from user.forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('profile')
        form = RegisterForm()
        return render(request, "user/register.html", {'form': form})

    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            login(request, user)
            return redirect('profile')
        return render(request, "user/register.html", {'form': form})

def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('profile')
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect('profile')
        return render(request, 'user/login.html', {'form': form})

class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'user/profile.html', {'user': request.user})
        else:
            return redirect('user/register.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    else:
        return redirect("register")