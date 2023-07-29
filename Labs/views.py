import datetime
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from Labs.helper import (
    IssuessHelper,
    DashBoardHelper,
    TeamsHelper,
    RolesHelper,
    UserDetailsHelper,
)
from roles.models import UserRole
from assets.models import Borrowed_Asset
from accounts.views import Labview
from workstudy.globalsettings import LOGIN_URL
from Labs.models import Issue, Lab


@login_required(login_url=LOGIN_URL)  # type: ignore
def dashboard_redirect(request):
    orgSelectedUUID = request.GET["orgSelected"]
    user = Account.get_account(request.user)
    if not user.is_supervisor:
        """
        Check user is not supervisor, display nomal user page
        else display supervisor admin
        """
        role = UserRole.check_user_schedule(user)
        if orgSelectedUUID and role:
            return redirect("dashboard", uuid=orgSelectedUUID)
        if orgSelectedUUID and not role:
            return redirect("pick my schedule", uuid=orgSelectedUUID)
        else:
            messages.info(request, "You did not select a workstudy location")
            return redirect(Labview)
    else:
        return redirect("admin_dashboard")


@login_required(login_url=LOGIN_URL)
def dashboard(request, uuid=None):
    helper = DashBoardHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    print(context)
    context["my_schedule"] = helper.latestSchdule()
    context["issues"] = Issue.getUserList(request.user)
    context["borrowedItems"] = Borrowed_Asset.getBorrowedAssets(uuid)
    return render(request, "team/dashboard.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def roles(request, uuid):
    helper = RolesHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    context["roles"] = helper.get_roles()
    return render(request, "team/roles.html", context=context)


@login_required(login_url=LOGIN_URL)
def myteam(request, uuid):
    helper = TeamsHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    context["team"] = helper.get_members()
    return render(request, "team/team.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def issues(request, uuid):
    page_number = 1
    if request.GET.get("page"):
        page_number = request.GET.get("page")
    helper = IssuessHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    issues = helper.getAllUserIssuesList()
    paginator = Paginator(issues, 5)
    page_obj = paginator.get_page(page_number)
    context["issues"] = page_obj
    return render(request, "team/issues.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def raiseIssue(request, uuid):
    # report and issue
    if request.method == "POST":
        details = request.POST["details"]
        status = request.POST["status"]
        title = request.POST["title"]
        now = datetime.datetime.now()
        try:
            reported_by = Account.get_account(request.user)
            lab = Lab.get_Labs_from_uuid(uuid)
            issue = Issue(
                Lab=lab,
                status=status,
                details=details,
                reported_on=now,
                reported_by=reported_by,
                title=title,
            )
            issue.save()
        except Exception as e:
            # unexpected error failing to save issue
            context = {
                "message": f"Please contact the devs and notify them of the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)
        else:
            messages.success(
                request, f"An issue has be raised by you, {reported_by.first_name}."
            )
            return redirect(issues, uuid=uuid)
    if request.method == "GET":
        helper = UserDetailsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        return render(request, "team/addissue.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def getIssueDetails(request, uuid, issue_pk):
    helper = IssuessHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    context["issue"] = Issue.getIssueByPk(issue_pk)
    return render(request, "team/issuedetails.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def profile(request, uuid=None):
    if request.method == "GET":
        
        helper = UserDetailsHelper(user=request.user, uuid=uuid)
        context = helper.get_profile()
        return render(request, "team/users-profile.html", context=context)
