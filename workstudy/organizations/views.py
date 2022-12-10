from django.shortcuts import redirect, render

from accounts.models import Account
from django.contrib.auth.decorators import login_required
from organizations.models import Organization
from accounts.views import organization
from workstudy.globalsettings import LOGIN_URL
from organizations.helper import TeamsHelper, UserDetailsHelper,RolesHelper

# Create your views here.


@login_required(login_url=LOGIN_URL)  # type: ignore
def dashboard_redirect(request):
    orgSelectedUUID = request.GET['orgSelected']
    if orgSelectedUUID:
        return redirect('dashboard',uuid = orgSelectedUUID)
    else:
        return redirect(organization)


@login_required(login_url=LOGIN_URL)
def dashboard(request,uuid):
    helper = UserDetailsHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    return render(request,"dashboard.html",context = context)



@login_required(login_url=LOGIN_URL)  # type: ignore
def roles(request,uuid):
    helper = RolesHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    context['roles'] = helper.get_roles()
    print(context)
    return render(request,"roles.html",context = context)
    


@login_required(login_url=LOGIN_URL)  # type: ignore
def myteam(request,uuid):
    helper = TeamsHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    return render(request,"team.html",context = context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def reports(request,uuid):
    pass


@login_required(login_url=LOGIN_URL)  # type: ignore
def profile(request,uuid):
    pass

@login_required(login_url=LOGIN_URL)  # type: ignore
def assets(request,uuid):
    return render(request,"assets.html")