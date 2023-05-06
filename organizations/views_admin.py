import datetime
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from accounts.views import organization
from organizations.helper_admin import *
from roles.models import UserRole
from assets.models import Borrowd_Asset

from workstudy.globalsettings import LOGIN_URL
from organizations.models import Issue, Organization

import logging

logger = logging.getLogger("django")


@login_required(login_url=LOGIN_URL)
def admin_dashboard(request, uuid):
    helper = UserAdminDetailsHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    return render(request, "admin_user/dashboard.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def admin_myteam(request, uuid):
    """
    list of user accounts who work in the organization
    """
    helper = TeamAdminHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    context["team"] = helper.get_members()
    return render(request, "admin_user/team.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def admin_roles(request, uuid):
    helper = RolesAdminHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    context["roles"] = helper.get_roles()
    return render(request, "admin_user/roles.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def admin_roles_form(request, uuid):
    if request.method == "GET":
        helper = RolesAdminHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        context["roles"] = helper.get_roles()
        return render(request, "admin_user/roleform.html", context=context)
    if request.method == "POST":
        try:
            roleTitle = request.POST["roleTitle"]
            organization_uuid = uuid
            description = request.POST["description"]
            task1 = request.POST["task1"]
            task2 = request.POST["task2"]
            task3 = request.POST["task3"]
            task4 = request.POST["task4"]
            task5 = request.POST["task6"]
            task6 = request.POST["task5"]

            new_role = Role(
                title=roleTitle,
                organization_id=organization_uuid,
                description=description,
                task_1=task1,
                task_2=task2,
                task_3=task3,
                task_4=task4,
                task_5=task5,
                task_6=task6,
            )
            new_role.save()
            messages.success(request, f"{roleTitle} has been created.")
            return redirect(admin_roles_form, uuid)
        except Exception as e:
            context = {
                "message": f"Please contact the devs and notify the off the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def admin_issues(request, uuid):
    page_number = 1
    if request.GET.get("page"):
        page_number = request.GET.get("page")
    helper = IssuessAdminHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    issues = helper.getAllIssuesList()
    paginator = Paginator(issues, 5)
    page_obj = paginator.get_page(page_number)
    context["issues"] = page_obj
    return render(request, "admin_user/issues.html", context=context)
