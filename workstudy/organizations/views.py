from django.shortcuts import redirect, render
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from accounts.views import organization
from organizations.helper import DashBoardHelper, TeamsHelper,RolesHelper
from roles.models import UserRole

from workstudy.globalsettings import LOGIN_URL
# Create your views here.


@login_required(login_url=LOGIN_URL)  # type: ignore
def dashboard_redirect(request):
    orgSelectedUUID = request.GET['orgSelected']
    user = Account.get_account(request.user)
    role = UserRole.check_user_schedule(user)
    if orgSelectedUUID and role:
        return redirect('dashboard',uuid = orgSelectedUUID)
    if orgSelectedUUID and not role:
        return redirect ('pick my schedule',uuid = orgSelectedUUID )
    else:
        return redirect(organization)


@login_required(login_url=LOGIN_URL)
def dashboard(request,uuid):
    helper = DashBoardHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    context["my_schedule"] = helper.latestSchdule()
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
    context['team'] = helper.get_members()
    return render(request,"team.html",context = context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def reports(request,uuid):
    pass


@login_required(login_url=LOGIN_URL)  # type: ignore
def profile(request,uuid):
    pass


    