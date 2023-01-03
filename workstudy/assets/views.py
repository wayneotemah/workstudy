from django.shortcuts import render,redirect
from assets.helper import AssetsHelper
from django.contrib.auth.decorators import login_required
from assets.models import Asset

from workstudy.globalsettings import LOGIN_URL
from organizations.models import Organization

# Create your views here.

@login_required(login_url=LOGIN_URL)  # type: ignore
def assets(request,uuid):
    helper = AssetsHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    context['assets'] = helper.getAssets()
    return render(request,"assets.html",context=context)



@login_required(login_url=LOGIN_URL)  # type: ignore
def post_asset(request,uuid):
    if request.method == "POST":
        organization = Organization.get_organizations_from_uuid(uuid)
        name = request.POST["asset_name"]
        condition = request.POST["condition"]
        status   = request.POST["status"]
        pic = request.FILES['asset_pic']

        asset = Asset(name = name,condition = condition,status = status,pic=pic,organization=organization)
        asset.save()
        return redirect('assets',uuid = uuid) 