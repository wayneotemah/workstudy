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
            messages.error(request, 'Wrong email and password.')
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
            return render(request, "createprofile.html", {"message": "Your account already exists."})

    elif request.method == "GET":
        return render(request, "createprofile.html")


@login_required(login_url=LOGIN_URL)  # type: ignore
def organization(request):
    try:
        # get the users account profile details
        user = Account.get_account(request.user)  # type: ignore
    except ObjectDoesNotExist as e:
        messages.info(
            request, 'It seems you dont have a profile, lets get that.')
        return render(request, "createprofile.html")

    organization_list = Organization.get_organizations(user)
    if not organization_list:
        # check if user has a role

        role = UserRole.getUserOrganizationRoles(user)
        if role:
            # use the user to get the organization

            organization_list = UserRole.getOrganization(user)
        else:
            messages.info(
                request, 'It seems you dont have a workstudy location.')

            context = {
                "message": "You have not been assigned to any workstudy location. Please contact you supervisor to add you to his/her location, the refresh the page"
            }
            return render(request, "errorpage.html", context=context)
    context = {
        "organization_name": organization_list.name,
        "organization_uuid": organization_list.organization_uuid
    }
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
            return render(request, "create_organization.html", {"message": e})
    elif request.method == "GET":
        try:
            # get the users account profile details
            user = Account.get_account(request.user)
            if user.is_supervisor:
                return render(request, "create_organization.html")
            elif not user.is_supervisor:
                return redirect(organization)

        except ObjectDoesNotExist as e:
            messages.info(
                request, 'It seems you dont have a profile, lets get that.')
            return render(request, "createprofile.html")




@login_required(login_url=LOGIN_URL)  # type: ignore
def account(request):
    return render(request, "users-profile.html")


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
            return render(request, "datepicker.html", context=context)
        else:
            # schedule is full redirect to dashboard
            uuid = UserRole.getOrganization(user).organization_uuid
            return redirect('dashboard', uuid=uuid)

    if request.method == "GET":
        context['schedule'] = UserRole.getUserSchedule(user)
        return render(request, "datepicker.html", context=context)


def logout_view(request):
    logout(request)
    return redirect('sign in')
