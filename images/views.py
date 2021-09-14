from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())


def index(request):
    return render(request,"images/index.html")

def login(request):

    if(request.method == "POST"):
        print("It was a post")
        #is form vaild
        #get data from form
        #login
        newUser = LoginForm(request.POST)
        if newUser.is_valid():
            username = newUser.cleaned_data["username"]
            password = newUser.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            print(username)
            print(password)


    return render(request,"images/login.html",{
        "form":LoginForm(),
    })

def logout(request):
    print("You have been logged out")
    return HttpResponseRedirect(reverse("index"))

def register(request):
    return render(request,"images/register.html",{
        "form":RegisterForm()
    })

def test(request):
    return HttpResponse("Hello This is the Test View")
