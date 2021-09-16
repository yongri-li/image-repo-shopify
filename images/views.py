from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import User, Image, Repo
import os
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
    private = forms.BooleanField()


def images(request,level):
    
    if level == "private":
        repos = Repo.objects.filter(
            author = request.user,private=True
        )
    elif level == "public":
        repos = Repo.objects.filter(
            private=False
        )
    elif level == "both":
        repos = Repo.objects.all()

    ans = []
    for repo in repos:
        ans.append(repo.serialize())

    return JsonResponse(ans,safe=False)
    


def index(request):
    #images = Image.objects.all()
    return render(request,"images/index.html")#,{
    #    "images":images
    #})


def create_view(request):
    #create a repo with a list of images
    if(request.method == "GET"):
        return render(request,"images/create_repo.html")

    elif(request.method == "POST" and request.user.is_authenticated):
        #make Repo object
        repoData = request.POST
        repoTitle = repoData["title"]
        repoDes = repoData["des"]
        repoPrivate = repoData.get('private',False) == "on"
        newRepo = Repo(title=repoTitle,description=repoDes,private=repoPrivate,author=request.user)
        newRepo.save()
        print(f"You just made a new Repo {newRepo}")
        #get list of images
        repoImages = request.FILES.getlist('images')
        for image in repoImages:
            imTitle = str(image).split(".")[0]
            newImage = Image(title=imTitle,image=image,repo=newRepo,author=request.user,private=repoPrivate)
            newImage.save()

        #make Image objects
        
        print("HELLo")



    

    return HttpResponseRedirect(reverse("index"))


def bulk_upload_view(request):
    if request.method == "POST" and request.user.is_authenticated:
        imageList = request.FILES.getlist('images')
        data = request.POST
        
        private = data.get('private',False) == "on"
        for image in imageList:
            #print()
            if len(Image.objects.filter(title=image)) == 0:
                theTitle = ""
                for c in str(image):
                    if(c == "."):
                        break
                    theTitle = theTitle + c
                newImage = Image(title=theTitle,image=image,author=request.user,private=private)
                newImage.save()
            else:
                print(f"{image} is already in database")


        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"images/bulk_upload.html")

def upload_view(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            theImage = Image(title=form.cleaned_data["title"],image=form.cleaned_data["image"],author=request.user,private=form.cleaned_data["private"])
            theImage.save()
    if request.user.is_authenticated:
        return render(request,"images/upload.html",{
            "form": ImageUploadForm()
        })
    else:
        return render(request,"images/upload.html")



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
