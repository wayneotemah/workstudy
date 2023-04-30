from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from accounts.models import Account, CustomUser
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from organizations.models import Organization
from workstudy.globalsettings import LOGIN_URL
from roles.models import UserRole

# Create your views here.


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(organization)
        else:
            messages.error(request, 'Wrong email or password.')
            return render(request, "pages-login.html")

    elif request.method == "GET":
        return render(request, "pages-login.html")


def sign_up(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.user_exists(email):
            messages.info(request, 'Your account already exists, please login')
            return render(request, "pages-login.html")

        else:
            
            """
            if user does not exist, save detail
            """

            phone_number = request.POST['phone_number']
            password = request.POST['password']
            try:
                user = CustomUser(email=email,
                                  phone_number=phone_number)
                user.set_password(password)
                user.save()
                if user is not None:
                    messages.info(request, 'Account created please login')
                    return render(request, "pages-login.html")
            except IntegrityError:
                messages.error(
                    request, 'Phone number already exists.')
                return render(request, "pages-register.html")
            else:
                """
                something went wront.
                """
                messages.warning(
                    request, 'Something went wrong while creating you account, Please infrom the admin or devs')
                return render(request, "pages-register.html")

    elif request.method == "GET":
        return render(request, "pages-register.html")


@login_required(login_url=LOGIN_URL)  # type: ignore
def createprofile(request):
    if request.method == "POST":
        user = request.user
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        try:
            newAccount = Account(last_name=lastName,
                                 first_name=firstName, user=user)
            newAccount.save()
            return redirect(organization)
        except IntegrityError:
            return render(request, "team/createprofile.html", {"message": "Your account already exists."})

    elif request.method == "GET":
        return render(request, "team/createprofile.html")


@login_required(login_url=LOGIN_URL)
def organization(request):
    try:
        # get the users account profile details
        user = Account.get_account(request.user) 
    except ObjectDoesNotExist as e:
        messages.info(
            request, 'It seems you dont have a profile, lets get that.')
        return render(request, "team/createprofile.html")

    print(user.is_supervisor)
    organization = Organization.get_organizations(user) # check if users is a supervisor
    if  not user.is_supervisor:  # user is not supervisor

        role = UserRole.getUserOrganizationRoles(user) # check if user has a role
        if role:
            # use the user to get the organization

            organization = UserRole.getOrganization(user)
            context = {
                "organization_name": organization.name,
                "organization_uuid": organization.organization_uuid
            }
            return render(request, "choose_organization.html", context=context)

        else:
            # if no roles, user has not be assigend to any work location
            messages.info(
                request, 'No work location🥲')
            context = {
                "message":"""It seems you dont have a workstudy location.Please contact you supervisor
                            to add you to his/her location, then refresh the page.
                            If you want to create an organization, contact the platform developers"""
            }
            return render(request, "errorpage.html", context=context)
    if  user.is_supervisor:  # user is supervisour

        if organization:
            

            context = {
                    "organization_name": organization.name,
                    "organization_uuid": organization.organization_uuid
                }
        else: 
            messages.info(request, "No organization, create one")
            context = {}
        return render(request, "choose_organization.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def create_organization(request):
    if request.method == "POST":
        organizationName = request.POST['organizationname']
        try:
            user = Account.get_account(request.user)
            newOrganization = Organization(
                name=organizationName, supervisor=user)
            newOrganization.save()
            return redirect(organization)
        except ObjectDoesNotExist as e:
            return render(request, "createprofile.html", {"message": "You do not have a profile, please create one"})
        except IntegrityError as e:
            messages.warning(request, "You already created this organization")
            return render(request, "create_organization.html", {"message": "Already exists"})
    elif request.method == "GET":
        try:
            # get the users account profile details
            user = Account.get_account(request.user)
            if user.is_supervisor: 
                # chech if user is a supervisor the allow them to create the organization

                return render(request, "create_organization.html")
            elif not user.is_supervisor:
                messages.info(request, 'No system privileges to create an ornanizations')
                return redirect(organization)

        except ObjectDoesNotExist as e:
            messages.info(
                request, 'It seems you dont have a profile, lets get that.')
            return render(request, "team/createprofile.html")




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
            return redirect('dashboard', uuid=uuid)
        start_time = request.POST["start_time"]
        end_time = request.POST["end_time"]
        addSchedule = UserRole.addToSchelule(
            account=user, start_time=start_time, end_time=end_time, day=day)
        if addSchedule:
            # schedule is not full
            messages.success(request, "Date and time was added successfully")
            context['schedule'] = UserRole.getUserSchedule(user)
            return render(request, "team/datepicker.html", context=context)
        else:
            # schedule is full redirect to dashboard
            uuid = UserRole.getOrganization(user).organization_uuid
            return redirect('dashboard', uuid=uuid)

    if request.method == "GET":
        context['schedule'] = UserRole.getUserSchedule(user)
        return render(request, "team/datepicker.html", context=context)


def logout_view(request):
    logout(request)
    return redirect('sign in')
