from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def sign_in(request):
    return render(request,"pages-login.html") 

def sign_up(request):
    return render(request,"pages-register.html")

def organization(request):
    return render(request,"choose_organization.html")

def create_organization(request):
    return render(request,"create_organization.html")

def account(request):
    return render(request,"users-profile.html")

def schedule(request):
    return render(request,"datepicker.html")