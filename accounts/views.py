from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from accounts.models import Account
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from Labs.models import Lab
from workstudy.globalsettings import LOGIN_URL
from roles.models import UserRole

import logging

logger = logging.getLogger("django")

# Create your views here.


@login_required(login_url=LOGIN_URL)  # type: ignore
def createprofile(request):
    if request.method == "POST":
        user = request.user
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        phone = request.POST["phone"]
        try:
            newAccount = Account(
                last_name=lastName,
                first_name=firstName,
                user=user,
            )
            newAccount.save()
            user.phone_number = phone
            user.save()
            return redirect(Labview)
        except IntegrityError:
            return render(
                request,
                "createprofile.html",
                {"message": "Your account already exists."},
            )

    elif request.method == "GET":
        user = request.user
        account_exists = SocialAccount.objects.filter(user=user).exists()
        if account_exists:
            name = SocialAccount.objects.get(user=user).extra_data["name"]
            firstName = name.split(" ")[0]
            lastName = name.split(" ")[1]
            Account.objects.create(
                user=user,
                first_name=firstName,
                last_name=lastName,
            )
            return redirect(Labview)
        else:
            messages.info(
                request,
                "It seems you dont have a profile, lets get that.",
            )
            return render(request, "createprofile.html")


@login_required(login_url=LOGIN_URL)
def Labview(request):
    try:
        # get the users account profile details
        user = Account.get_account(request.user)
    except ObjectDoesNotExist:
        return redirect("createprofile")

    logger.info(f"{request.user} is supervisor: {user.is_supervisor}")
    # supervisor_lab = Lab.get_Labs(user)  # check if users is a supervisor
    if not user.is_supervisor:  # user is not supervisor
        role = UserRole.getUserLabRoles(user)  # check if user has a role
        if role:
            # use the user to get the Lab

            user_lab = UserRole.getLab(user)
            context = {"Lab_name": user_lab.name, "Lab_uuid": user_lab.Lab_uuid}
            return render(request, "choose_Lab.html", context=context)

        else:
            # if no roles, user has not be assigend to any work location
            messages.info(request, "No work location🥲")
            context = {
                "message": """It seems you dont have a workstudy location.Please contact you supervisor
                            to add you to his/her location, then refresh the page.
                            If you want to create an Lab, contact the platform developers, <div><a href="/accounts/logout/"
                            >logout</a></div>"""
            }
            return render(request, "errorpage.html", context=context)
    if user.is_supervisor:  # user is supervisour
        return redirect("admin_dashboard")


@login_required(login_url=LOGIN_URL)  # type: ignore
def account(request):
    return render(request, "team/users-profile.html")


@login_required(login_url=LOGIN_URL)  # type: ignore
def schedule(request, uuid):
    user = Account.get_account(request.user)
    context = {}
    context["orgSelectedUUID"] = uuid

    if request.method == "POST":
        day = request.POST["day"]
        if not day:
            messages.warning(request, "The day field can not be emplty")
            return redirect("dashboard", uuid=uuid)
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        addSchedule = UserRole.addToSchelule(
            account=user, start_time=start_time, end_time=end_time, day=day
        )
        if addSchedule:
            # schedule is not full
            messages.success(request, "Date and time was added successfully")
            context["schedule"] = UserRole.getUserSchedule(user)
            return render(request, "team/datepicker.html", context=context)
        else:
            # schedule is full redirect to dashboard
            uuid = UserRole.getLab(user).Lab_uuid
            return redirect("dashboard", uuid=uuid)

    if request.method == "GET":
        context["schedule"] = UserRole.getUserSchedule(user)
        return render(request, "team/datepicker.html", context=context)


def logout_view(request):
    logout(request)
    return redirect("account")
