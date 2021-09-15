from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import User, Image
# Create your views here.

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

class ImageUploadForm(forms.Form):
    title = forms.CharField()
    image = forms.ImageField()




def index(request):
    images = Image.objects.all()
    return render(request,"images/index.html",{
        "images":images
    })

def upload_view(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            theImage = Image(title=form.cleaned_data["title"],image=form.cleaned_data["image"],author=request.user)
            theImage.save()
    if request.user.is_authenticated:
        return render(request,"images/upload.html",{
            "form": ImageUploadForm()
        })
    else:
        return render(request,"images/upload.html")

def bulk_upload_view(request):
    if request.method == "POST" and request.user.is_authenticated:
        imageList = request.FILES.getlist('images')

        for image in imageList:
            newImage = Image(title=image,image=image,author=request.user)
            newImage.save()


        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"images/bulk_upload.html")

def login_view(request):

    if(request.method == "POST"):
    
        newUser = LoginForm(request.POST)
        if newUser.is_valid():
            username = newUser.cleaned_data["username"]
            password = newUser.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "images/login.html", {
                    "form": LoginForm(),
                    "message": "Invalid username and/or password."
                })
    else:
        return render(request,"images/login.html",{
            "form":LoginForm(),
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if(request.method == "POST"):
        newUser = RegisterForm(request.POST)

        if newUser.is_valid():
            username = newUser.cleaned_data["username"]
            password = newUser.cleaned_data["password"]
            passwordCom = newUser.cleaned_data["password_confirm"]
            userEmail = newUser.cleaned_data["email"]
            if password != passwordCom:
                return render(request, "images/register.html", {
                    "message": "Passwords did not match.",
                    "form":RegisterForm()
                })
            try:
                user = User.objects.create_user(username, userEmail, password)
                user.save()
            except IntegrityError:
                return render(request, "images/register.html", {
                    "message": "Username already taken.",
                    "form":RegisterForm()
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"images/register.html",{
            "form":RegisterForm()
        })

def test(request):
    return HttpResponse("Hello This is the Test View")
