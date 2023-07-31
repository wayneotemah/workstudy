from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from roles.models import UserRole, Role
from assets.models import Borrowed_Asset
from datetime import datetime
from Labs.helper_admin import (
    TeamAdminHelper,
    IssuessAdminHelper,
    RolesAdminHelper,
    UserAdminDetailsHelper,
)
from Labs.models import Issue
from accounts.models import CustomUser
from Labs.models import Lab
from workstudy.globalsettings import LOGIN_URL
import logging
from lab_services.models import Found_Item


logger = logging.getLogger("django")


@login_required(login_url=LOGIN_URL)
def admin_dashboard(request, uuid=None):
    context = {}
    helper = UserAdminDetailsHelper(user=request.user, uuid=uuid)
    context["profile"] = helper.get_profile()
    context["lab_schedule"] = UserRole.get_current_shift_assignment()
    context["issues"] = Issue.objects.all()
    context["borrowedItems"] = Borrowed_Asset.objects.all()
    print(request.user.account.Lab.all())

    return render(request, "admin_user/dashboard.html", context=context)


@login_required(login_url=LOGIN_URL)
def admin_labs(request, uuid=None):
    if request.method == "GET":
        context = {}
        helper = UserAdminDetailsHelper(user=request.user, uuid=uuid)
        context["lab_schedule"] = UserRole.get_current_shift_assignment()
        context["profile"] = helper.get_profile()
        return render(request, "admin_user/lab.html", context=context)
    if request.method == "POST":
        LabName = request.POST["Labname"]

        newLab, created = Lab.objects.get_or_create(
            name=LabName, supervisor=request.user.account
        )
        if created:
            newLab.save()
            messages.success(request, "Lab has been created👍")
            return redirect(admin_labs)
        else:
            messages.info(request, "You already created this lab")
            return redirect(admin_labs)


@login_required(login_url=LOGIN_URL)
def admin_myteam(request, uuid=None):
    """
    list of user accounts who work in the Lab
    """
    context = {}
    context["team"] = UserRole.objects.filter(
        role__Lab__supervisor=request.user.account
    )
    return render(request, "admin_user/team.html", context)


@login_required(login_url=LOGIN_URL)
def new_members(request, uuid=None):
    """
    add a team to supervisors Lab
    """
    if request.method == "GET":
        helper = TeamAdminHelper(user=request.user, uuid=uuid)
        context = {}
        context["profile"] = helper.get_profile()
        context["accounts"] = helper.get_unassigned_user()
        context["roles"] = Role.objects.filter(Lab__supervisor=request.user.account)
        return render(
            request,
            "admin_user/addteammember.html",
            context=context,
        )
    if request.method == "POST":
        account_id = request.POST["account_uuid"]
        role_id = request.POST["role_id"]
        print(role_id)
        userrole = UserRole(role_id=role_id, assigned_to_id=account_id)
        userrole.save()
        messages.success(request, "Added new team member👍")
        return redirect(admin_myteam)


@login_required(login_url=LOGIN_URL)
def admin_member_profile(request, account_uuid, uuid=None):
    if request.method == "GET":
        helper = TeamAdminHelper(
            user=request.user, uuid=uuid, account_uuid=account_uuid
        )
        context = {}
        context["member_profile"] = helper.get_member_profile()
        return render(request, "admin_user/teamprofile.html", context=context)
    if request.method == "POST":
        if "accountStatus" in request.POST:
            active = True if request.POST["accountStatus"] == "on" else False
        else:
            active = False

        member_Custom_instance = CustomUser.objects.get(account=account_uuid)
        member_Custom_instance.is_active = active
        member_Custom_instance.save()
        state = "active" if active else "inactive"
        messages.success(request, f"User has been made {state}")
        return redirect(admin_member_profile, account_uuid, uuid)


@login_required(login_url=LOGIN_URL)
def admin_roles(request, uuid=None):
    if request.method == "GET":
        helper = RolesAdminHelper(user=request.user, uuid=uuid)
        context = {}
        context["profile"] = helper.get_profile()
        context["roles"] = Role.objects.filter(
            Lab__supervisor=request.user.account,
        )
        return render(request, "admin_user/roles.html", context=context)
    if request.method == "POST":
        try:
            roleTitle = request.POST["roleTitle"]
            Lab_uuid = request.POST["lab_id"]
            description = request.POST["description"]
            task1 = request.POST["task1"]
            task2 = request.POST["task2"]
            task3 = request.POST["task3"]
            task4 = request.POST["task4"]
            task5 = request.POST["task6"]
            task6 = request.POST["task5"]

            new_role = Role(
                title=roleTitle,
                Lab_id=Lab_uuid,
                description=description,
                task_1=task1,
                task_2=task2,
                task_3=task3,
                task_4=task4,
                task_5=task5,
                task_6=task6,
            )
            new_role.save()
            messages.success(request, f"{roleTitle} has been created. 👍")
            return redirect(admin_roles)
        except Exception as e:
            context = {
                "message": f"Please contact the devs and notify them of the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)


@login_required(login_url=LOGIN_URL)
def admin_issues(request, uuid=None):
    page_number = 1
    if request.GET.get("page"):
        page_number = request.GET.get("page")
    helper = IssuessAdminHelper(user=request.user, uuid=uuid)
    context = {}
    context["profile"] = helper.get_profile()
    issues = Issue.objects.filter(
        Lab__supervisor=request.user.account,
    )
    paginator = Paginator(issues, 5)
    page_obj = paginator.get_page(page_number)
    context["issues"] = page_obj
    return render(request, "admin_user/issues.html", context=context)


@login_required(login_url=LOGIN_URL)
def admin_IssueDetails(request, issue_pk, uuid=None):
    # try:
        if request.method == "GET":
            helper = IssuessAdminHelper(user=request.user, uuid=uuid)
            context = {}
            context["profile"] = helper.get_profile()
            context["issue"] = Issue.getIssueByPk(issue_pk)
            return render(
                request,
                "admin_user/issuedetails.html",
                context,
            )
        elif request.method == "POST":
            issue = Issue.getIssueByPk(issue_pk)
            issue.status = request.POST["issue_status"]
            issue.admin_response = request.POST["admin_response"]
            if request.POST["issue_status"] == "Done":
                issue.addressed_on = datetime.now()

            issue.save()
            return redirect(admin_IssueDetails, issue_pk)
    # except Exception as e:
    #     context = {
    #         "message": f"Please contact the devs and notify them of the error \nerror is: \n{e}"
    #     }
    #     messages.warning(request, "Unexpected Exception error has risen")
    #     return render(request, "errorpage.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def admin_profile(request, uuid=None):
    if request.method == "GET":
        helper = UserAdminDetailsHelper(user=request.user, uuid=uuid)
        context = helper.get_profile()
        context["profile"] = helper.get_profile()
        return render(request, "admin_user/users-profile.html", context)


@login_required(login_url=LOGIN_URL)
def admin_lost_and_found(request):
    """
    get the list of lost and found assets for the supervisor view
    """
    if request.method == "GET":
        found_items = Found_Item.objects.all()

        # Include the found items data in the template context
        context = {
            "found_items_data": found_items,
        }

        return render(request, "admin_user/lost_and_found.html", context)
    if request.method == "POST":
        lab_id = request.POST.get("lab")
        item_name = request.POST.get("item_name")
        item_description = request.POST.get("item_description")
        time_found = request.POST.get("time_found")
        item_photo = request.FILES.get("item_photo")

        lab = Lab.objects.get(pk=lab_id)

        Found_Item.objects.create(
            lab=lab,
            item_name=item_name,
            item_description=item_description,
            time_found=time_found,
            item_photo=item_photo,
        )
        return redirect(
            "admin lost and found"
        )  # Redirect to a success page after successful form submission
