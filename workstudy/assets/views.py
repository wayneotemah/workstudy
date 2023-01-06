import datetime

from django.shortcuts import render,redirect
from assets.helper import AssetsHelper
from django.contrib.auth.decorators import login_required
from assets.models import Asset, Borrowd_Asset

from workstudy.globalsettings import LOGIN_URL
from organizations.models import Organization

# Create your views here.

@login_required(login_url=LOGIN_URL)  # type: ignore
def assets(request,uuid):
    helper = AssetsHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    context['assets'] = helper.getAssets()
    return render(request,"assets.html",context=context)




@login_required(login_url=LOGIN_URL)# type: ignore
def borrowed_assets(request,uuid):
    if request.method == "GET":
        helper = AssetsHelper(user = request.user,uuid = uuid )
        context = helper.get_nav_details()
        context['borrowed_assets'] = helper.getBorrowesAssets()
        context['assets'] = helper.getAvailbleAssets()
        return render(request,"borrowed.html",context=context)
    if request.method == "POST":
        #posting borrowed item
        now = datetime.datetime.now()


        organization = Organization.get_organizations_from_uuid(uuid)#get organization instance from uuil 
        asset = Asset.getSingleAsset(request.POST["Item_id"]) # get asset instance from asset pk

        try:
            organization_id = organization
            person   = request.POST["persons_name"]
            contacts   = request.POST["persons_contacts"]
            location_of_use   = request.POST["locatio_of_use"]

            borroweditem = Borrowd_Asset(asset = asset,organization_id = organization_id,person = person, contacts = contacts, location_of_use = location_of_use, picked_on = now)
            borroweditem.returned = False
            borroweditem.save()
        except Exception as e:
            context={
                "errorTitle":"Exeption error Please contact you developerd",
                "message":f"error is {e}"
            }
            return render(request,"errorpage.html",context=context)
        else:
            asset.status = "Borrowed"
            asset.save()

        return redirect('borrowed assets',uuid = uuid) 



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


@login_required(login_url=LOGIN_URL) # type: ignore
def return_asset(request,borrowedasset_id,uuid):
    borrowed_item = Borrowd_Asset.getSingleBorrowedAssets(borrowedasset_id)
    borrowed_item.returned = True
    borrowed_item.returned_on = datetime.datetime.now()
    borrowed_item.save()

    asset = borrowed_item.asset
    asset.status = "Available"
    asset.save()

    return redirect('borrowed assets',uuid = uuid) 
    
    
    pass

    