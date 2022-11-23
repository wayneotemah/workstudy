from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from accounts.models import CustomUser



# Create your views here.

def sign_in(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect(account)
        else:
            return render(request,"pages-login.html",{'message':"incorrect login"})
            # Return an 'invalid login' error message.

    elif request.method == "GET":        
        return render(request,"pages-login.html") 

def sign_up(request):
    if request.method =='POST':
        email = request.POST['email']
        user = CustomUser.get_user(email)
        if not user:
            phone_number = request.POST['phone_number']
            password = request.POST['password']
            user = CustomUser(  email = email,
                                phone_number = phone_number)
            user.set_password(password)
            user.save()
            if user is not None:
                return redirect(sign_in)
            else:
                return render(request,"pages-register.html",{'message':"Error creating user, try again or call support"})
        else: 
            return render(request,"pages-login.html",{'message':"Email exists, please login"})
        
    elif request.method == "GET":
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