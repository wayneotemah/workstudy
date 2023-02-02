import datetime

from django.contrib import messages
from django.db import IntegrityError

from django.shortcuts import render, redirect
from assets.helper import AssetsHelper
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from assets.models import *

from workstudy.globalsettings import LOGIN_URL
from organizations.models import Organization


@login_required(login_url=LOGIN_URL)  # type: ignore
def assets(request, uuid):
    # get all assets for the organisation/lab
    page_number = 1
    if request.GET.get('page'):
        page_number = request.GET.get('page')

    helper = AssetsHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    assets = helper.getAssetCategoryList()
    paginator = Paginator(assets, 5)
    page_obj = paginator.get_page(page_number)
    context['assets'] = page_obj
    return render(request, "assets.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def borrowed_assets(request, uuid):
    if request.method == "GET":
        # get list of all borrowed item in that organization
        page_number = 1
        if request.GET.get('page'):
            page_number = request.GET.get('page')
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        borrowed_assets = helper.getBorrowesAssets()
        paginator = Paginator(borrowed_assets, 5)
        page_obj = paginator.get_page(page_number)
        context['borrowed_assets'] = page_obj
        return render(request, "borrowed.html", context=context)
    if request.method == "POST":
        # posting borrowed item
        now = datetime.datetime.now()

        organization = Organization.get_organizations_from_uuid(
            uuid)  # get organization instance from uuil
        # get asset instance from asset pk
        asset = Asset.getSingleAsset(request.POST["Item_id"])

        try:
            organization_id = organization
            person = request.POST["persons_name"]
            contacts = request.POST["persons_contacts"]
            location_of_use = request.POST["location_of_use"]

            borroweditem = Borrowd_Asset(asset=asset, organization_id=organization_id,
                                         person=person, contacts=contacts, location_of_use=location_of_use, picked_on=now)
            borroweditem.returned = False
            borroweditem.save()
        except Exception as e:
            # unexpected error failing to save borrowed item and asset tables
            context = {
                "message": f"Please contact the devs and notify the off the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)
        else:
            # successfully added item on
            asset.status = "Borrowed"
            asset.save()
            messages.success(request, f"{asset.name} borrowed successfully")
            return redirect('borrowed assets', uuid=uuid)


@login_required(login_url=LOGIN_URL)  # type: ignore
def borrowed_assets_page(request, uuid):
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        context['assets'] = helper.getAvailbleAssets()
        return render(request, "addborrowed.html", context=context)


@login_required(login_url=LOGIN_URL)  # type: ignore
def post_asset(request, uuid):
    # get asset posting page
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        return render(request, "addasset.html", context=context)

    if request.method == "POST":
        # adding asset
        now = datetime.datetime.now()

        name = request.POST["asset_name"]
        condition = request.POST["condition"]
        status = request.POST["status"]
        category_type = request.POST['category_type']
        pic = request.FILES['asset_pic']
        try:
            # try to save
            category = AssetCategory.getCategoryByName(
                category_type)  # get the asset instance
            organization = Organization.get_organizations_from_uuid(
                uuid)  # get organization instance for saving
            asset = Asset(category_type=category, name=name, condition=condition,
                          status=status, pic=pic, organization=organization)
            asset.save()
        except Exception as e:
            # if anything fails, show error page wtth message
            context = {
                "message": f"Please contact the devs and notify the off the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)
        else:
            # everthing was successful
            messages.success(request, f"{name} Added successfully")
            return redirect('assets', uuid=uuid)


@login_required(login_url=LOGIN_URL)
def assetCategory(request, uuid):
    '''
    Get-> get asset category list
    post-> add asset category to asset category list
    '''
    if request.method == "GET":
        page_number = 1
        if request.GET.get('page'):
            page_number = request.GET.get('page')

        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        assets = helper.getAssetCategoryList()
        paginator = Paginator(assets, 5)
        page_obj = paginator.get_page(page_number)
        context['assets'] = page_obj
        return render(request, "categoryassets.html", context=context)
    elif request.method == "POST":
        category = request.POST["category_type"]
        pic = request.FILES['asset_category_pic']
        try:
            categoryItem = AssetCategory(
                
                category=category,
                category_pic=pic,
                organization_id=uuid)
            categoryItem.save()
            return redirect(assetCategory, uuid=uuid)

        except IntegrityError as e:
            messages.warning(request, e)
            return render(request, "errorpage.html", context=context)

        except Exception as e:
            # if anything fails, show error page wtth message
            context = {
                "message": f"Please contact the devs and notify the off the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)


def postassetCategory(request, uuid):
    '''
    returns page with post asset form
    '''
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        return render(request, "addassetcategory.html", context=context)


def categoryDetails(request, uuid, cat_id):
    pass


@login_required(login_url=LOGIN_URL)  # type: ignore
def return_asset(request, borrowedasset_id, uuid):
    # returning the assets borrowed
    now = datetime.datetime.now()
    try:
        # try geting the item borrowd by it index
        borrowed_item = Borrowd_Asset.getSingleBorrowedAssets(borrowedasset_id)
        borrowed_item.returned = True  # turn returned to tru
        borrowed_item.returned_on = now  # set time returned to now
        borrowed_item.save()  # save
    except Exception as e:
        # if savig fails, show error page it message
        context = {
            "message": f"Please contact the devs and notify the off the error \nerror is: \n{e}"
        }
        messages.warning(request, "Unexpected Exception error has risen")
        return render(request, "errorpage.html", context=context)

    else:
        # everthing worked out, the
        asset = borrowed_item.asset  # get the asset instance
        asset.status = "Available"  # Turn status to availbe
        asset.save()  # save the asset instance
        messages.info(
            request, f"{borrowed_item.asset.name} return successfully")
        return redirect('borrowed assets', uuid=uuid)


@login_required(login_url=LOGIN_URL)  # type: ignore
def getAssetDetails(request, uuid, asset_pk):
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        item = Borrowd_Asset.getAssetByPK(asset_pk)
        if item:  # it the item existes in the borrowed table
            context['borrowed_item'] = Borrowd_Asset.getAssetByPK(asset_pk)
            return render(request, 'borrowed_asset_details.html', context=context)
        else:  # the item does not exist in the borrowed table seach in item talbe
            item = Asset.getSingleAsset(asset_pk)
            context['item'] = item
            return render(request, 'item_asset_details.html', context=context)