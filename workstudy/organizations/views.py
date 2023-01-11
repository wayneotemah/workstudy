import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from accounts.views import organization
from organizations.helper import IssuessHelper, DashBoardHelper, TeamsHelper,RolesHelper, UserDetailsHelper
from roles.models import UserRole
from assets.models import Borrowd_Asset

from workstudy.globalsettings import LOGIN_URL
from organizations.models import Issue, Organization
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
        messages.info(request,'You did not select a workstudy location')
        return redirect(organization)


@login_required(login_url=LOGIN_URL)
def dashboard(request,uuid):
    helper = DashBoardHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    context["my_schedule"] = helper.latestSchdule()
    context["issues"] =  Issue.getList(uuid)
    context["borrowedItems"] = Borrowd_Asset.getBorrowedAssets(uuid)
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
def issues(request,uuid):
    helper = IssuessHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    context['issues'] = helper.getAllIssuesList()
    return render(request,"issues.html",context = context)




@login_required(login_url=LOGIN_URL) # type: ignore
def raiseIssue(request,uuid):
    # report and issue
    if request.method == "POST":
        details = request.POST["details"]
        status = request.POST["status"]
        now = datetime.datetime.now()
        try:
            reported_by = Account.get_account(request.user)
            organization = Organization.get_organizations_from_uuid(uuid)
            issue = Issue(organization = organization,status = status, details = details,reported_on = now,reported_by = reported_by)
            issue.save()
        except Exception as e:
            # unexpected error failing to save issue
            context={
                "message":f"Please contact the devs and notify the off the error \nerror is: \n{e}"
            }
            messages.warning(request,"Unexpected Exception error has risen")
            return render(request,"errorpage.html",context=context)
        else:
            messages.success(request,f"An issue has be raise by you, {reported_by.first_name}.") 
            return redirect(issues, uuid = uuid)
    if request.method == "GET":
        helper = UserDetailsHelper(user = request.user,uuid = uuid )
        context = helper.get_nav_details()
        return render(request,"addissue.html", context=context )

@login_required(login_url=LOGIN_URL)  # type: ignore
def reports(request,uuid):
    
    pass



@login_required(login_url=LOGIN_URL)  # type: ignore
def profile(request,uuid):
     if request.method == "GET":
        helper = UserDetailsHelper(user = request.user,uuid = uuid )
        context = helper.get_profile()
        # context["profile"] = help.get_profile()
        return render(request,"users-profile.html", context=context )


    