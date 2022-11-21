from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login



# Create your views here.

def sign_in(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['email']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(account)
        else:
            return render(request,"pages-login.html",{'message':"incorrect login"})
            # Return an 'invalid login' error message.

    elif request.method == "GET":        
        return render(request,"pages-login.html") 

def sign_up(request):
    return render(request,"pages-register.html")

@login_required
def organization(request):
    return render(request,"choose_organization.html")

@login_required
def create_organization(request):
    return render(request,"create_organization.html")


@login_required
def account(request):
    return render(request,"users-profile.html")

@login_required
def schedule(request):
    return render(request,"datepicker.html")