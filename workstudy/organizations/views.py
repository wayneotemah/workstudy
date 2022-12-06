from django.shortcuts import redirect, render

from accounts.models import Account
from django.contrib.auth.decorators import login_required
from organizations.models import Organization
from workstudy.globalsettings import LOGIN_URL
from organizations.helper import UserDetailsHelper,RolesHelper

# Create your views here.


@login_required(login_url=LOGIN_URL)  # type: ignore
def dashboard_redirect(request):
    orgSelectedUUID = request.GET['orgSelected']
    if orgSelectedUUID:
        return redirect('dashboard',uuid = orgSelectedUUID)
    else:
        pass


@login_required(login_url=LOGIN_URL)
def dashboard(request,uuid):
    data = UserDetailsHelper(user = request.user,uuid = uuid )
    context = data.get_nav_details()
    return render(request,"dashboard.html",context = context)



@login_required(login_url=LOGIN_URL)  # type: ignore
def roles(request,uuid):
    data = RolesHelper(user = request.user,uuid = uuid )
    context = data.get_nav_details()
    return render(request,"roles.html",context = context)
    


@login_required(login_url=LOGIN_URL)  # type: ignore
def myteam(request,uuid):
    pass


@login_required(login_url=LOGIN_URL)  # type: ignore
def reports(request,uuid):
    pass


@login_required(login_url=LOGIN_URL)  # type: ignore
def profile(request,uuid):
    pass

@login_required(login_url=LOGIN_URL)  # type: ignore
def assets(request,uuid):
    return render(request,"assets.html")