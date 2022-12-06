from django.shortcuts import redirect, render

from accounts.models import Account
from django.contrib.auth.decorators import login_required
from organizations.models import Organization
from workstudy.globalsettings import LOGIN_URL

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
    organizationName  = Organization.objects.get(organization_uuid = uuid )


    userAccount = Account.get_account(request.user)
    username = " ".join([userAccount.first_name,userAccount.last_name])  # type: ignore

    context = {
        "username":username,
        "organizationName":organizationName
    }
    
    return render(request,"dashboard.html",context = context)


def assets(request):
    return render(request,"assets.html")