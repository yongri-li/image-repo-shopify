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
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class ImageUploadForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

class ImageEditForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


def index(request):
    return render(request,"images/index.html")
    
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
        newRepo = Repo(thumbnail=request.FILES.get("thumbnail"),title=repoTitle,description=repoDes,private=repoPrivate,author=request.user)
        newRepo.save()
        
        repoImages = request.FILES.getlist('images')
        for image in repoImages:
            imTitle = str(image).split(".")[0]
            newImage = Image(title=imTitle,image=image,repo=newRepo,author=request.user,private=repoPrivate)
            newImage.save()

    return HttpResponseRedirect(reverse("index"))

def repo_detail_view(request,pk):
    theRepo = Repo.objects.get(id=pk)
    
    if theRepo.private == False or request.user == theRepo.author:
        return render(request,"images/repo_detail.html")
    else:
        return HttpResponseRedirect(reverse("index"))

def get_repo_details(request,pk):
    theRepo = Repo.objects.get(id=pk)
    if theRepo.private == True and theRepo.author != request.user:
        return JsonResponse({"error": "This repo is private"},status=400)


    repoImages = Image.objects.filter(repo=theRepo)
    ans = {}
    for image in repoImages:
        ser = image.serialize()
        ans[ser["title"]] = ser
    return JsonResponse({"repo":theRepo.serialize(),"images":ans,"user":f"{request.user}"},safe=False)

def delete_image(request,pk):
    theImage = Image.objects.get(id=pk)
    if theImage.author != request.user:
        return JsonResponse({"error": "This is not your image"},status=400)
    theImage.delete()
    return JsonResponse(f"{theImage} was deleted",safe=False)

def delete_repo(request,pk):
    theRepo = Repo.objects.get(id=pk)
    if(theRepo.author == request.user):
        theRepo.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return JsonResponse({"error": "This is not your repo"},status=400)

def edit_image(request,pk):
    theImage = Image.objects.get(id=pk)
    if(theImage.author == request.user and request.method == "GET"):
        return render(request,"images/image_edit.html", {
            "image":theImage,
            "form":ImageEditForm()
        })
    elif(theImage.author == request.user and request.method == "POST"):
        imageEdit = ImageEditForm(request.POST)
        if(imageEdit.is_valid()):

            theImage.title = imageEdit.cleaned_data["title"]
            theImage.save()
        return HttpResponseRedirect(reverse("detail",kwargs={'pk':theImage.repo.id}))
    else:
       return JsonResponse({"error": "This is not your image"},status=400)


def images(request,level):
    
    if level == "private":
        repos = Repo.objects.filter(
            author = request.user,private=True
        )
    elif level == "public":
        repos = Repo.objects.filter(
            private=False
        )
    repos = repos.order_by("-timestamp").all()
    ans = []
    for repo in repos:
        ans.append(repo.serialize())

    return JsonResponse(ans,safe=False)

def bulk_upload_view(request,pk):
    theRepo = Repo.objects.get(id=pk)
    if request.method == "POST" and request.user.is_authenticated and request.user == theRepo.author:
        imageList = request.FILES.getlist('images')
        data = request.POST
        
        #private = data.get('private',False) == "on"
        for image in imageList:
            if len(Image.objects.filter(title=image)) == 0:
                theTitle = ""
                for c in str(image):
                    if(c == "."):
                        break
                    theTitle = theTitle + c
                newImage = Image(repo=theRepo,title=theTitle,image=image,author=request.user,private=theRepo.private)
                newImage.save()
            else:
                print(f"{image} is already in database")


        return HttpResponseRedirect(reverse("detail",kwargs={'pk':pk}))
    elif request.user.is_authenticated and theRepo.author == request.user:
        return render(request,"images/bulk_upload.html",{
            "repo":theRepo
        })
    else:
        return JsonResponse({"error":"This is not your Repo"},status=400)

def upload_view(request,pk):
    theRepo = Repo.objects.get(id=pk)
    
    if request.method == "POST" and request.user.is_authenticated and theRepo.author == request.user:
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            theImage = Image(repo=theRepo,title=form.cleaned_data["title"],image=form.cleaned_data["image"],author=request.user,private=theRepo.private)
            theImage.save()
            return HttpResponseRedirect(reverse("detail",kwargs={'pk':pk}))
    elif request.user.is_authenticated and theRepo.author == request.user:
        return render(request,"images/upload.html",{
            "form": ImageUploadForm(),
            "repo":theRepo
        })
    else:
        return JsonResponse({"error":"This is not your Repo"},status=400)



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

