import datetime

from django.contrib import messages
from django.shortcuts import render,redirect
from assets.helper import AssetsHelper
from django.contrib.auth.decorators import login_required
from assets.models import Asset, Borrowd_Asset

from workstudy.globalsettings import LOGIN_URL
from organizations.models import Organization

# Create your views here.

@login_required(login_url=LOGIN_URL)  # type: ignore
def assets(request,uuid):
    # get all assets for the organisation/lab
    helper = AssetsHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    context['assets'] = helper.getAssets()
    return render(request,"assets.html",context=context)

@login_required(login_url=LOGIN_URL)# type: ignore
def borrowed_assets(request,uuid):
    if request.method == "GET":
        #get list of all borrowed item in that organization
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
            location_of_use   = request.POST["location_of_use"]

            borroweditem = Borrowd_Asset(asset = asset,organization_id = organization_id,person = person, contacts = contacts, location_of_use = location_of_use, picked_on = now)
            borroweditem.returned = False
            borroweditem.save()
        except Exception as e:
            # unexpected error failing to save borrowed item and asset tables
            context={
                "message":f"Please contact the devs and notify the off the error \nerror is: \n{e}"
            }
            messages.warning(request,"Unexpected Exception error has risen")
            return render(request,"errorpage.html",context=context)
        else:
            # successfully added item on 
            asset.status = "Borrowed"
            asset.save()
            messages.success(request,f"{asset.name} borrowed successfully")
            return redirect('borrowed assets',uuid = uuid) 


@login_required(login_url=LOGIN_URL)  # type: ignore
def post_asset(request,uuid):
    if request.method == "POST":
        #adding asset
        now = datetime.datetime.now()

        name = request.POST["asset_name"]
        condition = request.POST["condition"]
        status   = request.POST["status"]
        pic = request.FILES['asset_pic']
        try:
            #try to save
            organization = Organization.get_organizations_from_uuid(uuid) #get organization instance for saving
            asset = Asset(name = name,condition = condition,status = status,pic=pic,organization=organization)
            asset.save()
        except Exception as e:
            #if anything fails, show error page it message 
            context={
                    "message":f"Please contact the devs and notify the off the error \nerror is: \n{e}"
                }
            messages.warning(request,"Unexpected Exception error has risen")
            return render(request,"errorpage.html",context=context)
        else:
            #everthing was successful
            messages.success(request,f"{name} Added successfully")
            return redirect('assets',uuid = uuid) 


@login_required(login_url=LOGIN_URL) # type: ignore
def return_asset(request,borrowedasset_id,uuid):
    #returning the assets borrowed
    now = datetime.datetime.now()
    try:
        #try geting the item borrowd by it index
        borrowed_item = Borrowd_Asset.getSingleBorrowedAssets(borrowedasset_id)
        borrowed_item.returned = True # turn returned to tru
        borrowed_item.returned_on = now #set time returned to now 
        borrowed_item.save() #save
    except Exception as e:
        #if savig fails, show error page it message
        context={
                "message":f"Please contact the devs and notify the off the error \nerror is: \n{e}"
            }
        messages.warning(request,"Unexpected Exception error has risen")
        return render(request,"errorpage.html",context=context)

    else:
        # everthing worked out, the 
        asset = borrowed_item.asset #get the asset instance
        asset.status = "Available" # Turn status to availbe
        asset.save() # save the asset instance
        messages.success(request,f"{borrowed_item.asset.name} return successfully")
        return redirect('borrowed assets',uuid = uuid) 
    