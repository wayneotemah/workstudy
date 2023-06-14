import datetime

from django.contrib import messages
from django.db import IntegrityError

from django.shortcuts import render, redirect
from assets.helper import AssetsHelper
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from assets.models import AssetCategory, Asset, Borrowed_Asset

from workstudy.globalsettings import LOGIN_URL


@login_required(login_url=LOGIN_URL)
def assets(request, uuid):
    # get all assets for the organisation/lab
    page_number = 1
    if request.GET.get("page"):
        page_number = request.GET.get("page")

    helper = AssetsHelper(user=request.user, uuid=uuid)
    context = helper.get_nav_details()
    assets = helper.getAssetCategoryList()
    paginator = Paginator(assets, 5)
    page_obj = paginator.get_page(page_number)
    context["assets"] = page_obj
    return render(request, "team/assets.html", context=context)


@login_required(login_url=LOGIN_URL)
def borrowed_assets(request, uuid):
    if request.method == "GET":
        # get list of all borrowed item in that Lab
        page_number = 1
        if request.GET.get("page"):
            page_number = request.GET.get("page")
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        borrowed_assets = helper.getBorrowesAssets()
        paginator = Paginator(borrowed_assets, 5)
        page_obj = paginator.get_page(page_number)
        context["borrowed_assets"] = page_obj
        return render(request, "team/borrowed.html", context=context)
    if request.method == "POST":
        # posting borrowed item
        now = datetime.datetime.now()
        # get asset instance from asset pk
        asset = Asset.getSingleAsset(request.POST["Item_id"])

        try:
            person = request.POST["persons_name"]
            contacts = request.POST["persons_contacts"]
            location_of_use = request.POST["location_of_use"]
            student_id = request.POST["student_id_number"]

            borroweditem = Borrowed_Asset(
                asset=asset,
                lab_id=uuid,
                person=person,
                contacts=contacts,
                location_of_use=location_of_use,
                picked_on=now,
                issued_out_by=request.user.account,
                student_id=student_id
            )
            borroweditem.returned = False
            borroweditem.save()
        except Exception as e:
            # unexpected error failing to save borrowed item and asset tables
            context = {
                "message": f"Please contact the devs and notify them of the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)
        else:
            # successfully added item on
            asset.status = "Borrowed"
            asset.save()
            AssetCategory.add_borrowed_assets(asset, uuid)
            messages.success(request, f"{asset.name} borrowed successfully")
            return redirect("borrowed assets", uuid=uuid)


@login_required(login_url=LOGIN_URL)
def borrowed_assets_page(request, uuid):
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        context["assets"] = helper.getAvailbleAssets()
        return render(request, "team/addborrowed.html", context=context)


@login_required(login_url=LOGIN_URL)
def post_asset(request, uuid, category_pk):
    # get asset posting page
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        context["category_pk"] = category_pk
        return render(request, "team/addasset.html", context=context)
    if request.method == "POST":
        # adding asset

        name = request.POST["asset_name"]
        condition = request.POST["condition"]
        status = request.POST["status"]
        pic = request.FILES["asset_pic"]
        try:
            # try to save
            # category = AssetCategory.getCategoryByName(
            #     category_type)  # get the asset instance
            # Lab = Lab.get_Labs_from_uuid(
            #     uuid)  # get Lab instance for saving
            asset = Asset(
                category_type_id=category_pk,
                name=name,
                condition=condition,
                status=status,
                pic=pic,
                Lab_id=uuid,
            )
            asset.save()
        except Exception as e:
            # if anything fails, show error page wtth message
            context = {
                "message": f"Please contact the devs and notify them of the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)
        else:
            # everthing was successful
            messages.success(request, f"{name} Added successfully")
            return redirect(
                getAssetCategoryDetails,
                uuid=uuid,
                category_pk=category_pk,
            )


@login_required(login_url=LOGIN_URL)
def assetCategory(request, uuid):
    """
    Get-> get asset category list
    post-> add asset category to asset category list
    """
    if request.method == "GET":
        page_number = 1
        if request.GET.get("page"):
            page_number = request.GET.get("page")

        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        assets = helper.getAssetCategoryList()
        paginator = Paginator(assets, 5)
        page_obj = paginator.get_page(page_number)
        context["assets"] = page_obj
        return render(request, "team/categoryassets.html", context=context)
    elif request.method == "POST":
        category = request.POST["category_type"]
        pic = request.FILES["asset_category_pic"]
        try:
            categoryItem = AssetCategory(
                category=category, category_pic=pic, Lab_id=uuid
            )
            categoryItem.save()
            return redirect(assetCategory, uuid=uuid)

        except IntegrityError as e:
            messages.warning(request, e)
            return render(request, "errorpage.html", context=context)

        except Exception as e:
            # if anything fails, show error page wtth message
            context = {
                "message": f"""
                            Please contact the devs and notify them of the error.
                            Error is: \n{e}
                            """
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)


@login_required(login_url=LOGIN_URL)
def postassetCategory(request, uuid):
    """
    returns page with post asset form
    """
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        return render(request, "team/addassetcategory.html", context=context)


@login_required(login_url=LOGIN_URL)
def assetDetails(request, uuid, item_pk):
    """
    show detils assets
    """
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        item = helper.getAssetDetails(item_pk)
        item_borrowed_details = Borrowed_Asset.objects.filter(asset=item).last()
        context["item"] = item

        if item_borrowed_details is not None:
            context["borrowed_item"] = item_borrowed_details

        return render(request, "team/item_asset_details.html", context=context)


@login_required(login_url=LOGIN_URL)
def return_asset(request, borrowedasset_id, uuid):
    # returning the assets borrowed
    now = datetime.datetime.now()
    try:
        # try geting the item borrowd by it index
        borrowed_item = Borrowed_Asset.getSingleBorrowedAssets(borrowedasset_id)
        borrowed_item.returned = True  # turn returned to true
        borrowed_item.returned_on = now  # set time returned to now
        borrowed_item.received_by = request.user.account
        borrowed_item.save()  # save

    except Exception as e:
        # if savig fails, show error page it message
        context = {
            "message": f"Please contact the devs and notify them of the error \nerror is: \n{e}"
        }
        messages.warning(request, "Unexpected Exception error has risen")
        return render(request, "errorpage.html", context=context)

    else:
        # everthing worked out, the
        asset = borrowed_item.asset  # get the asset instance
        asset.status = "Available"  # Turn status to availbe
        asset.save()  # save the asset instance
        AssetCategory.reduce_borrowed_assets(borrowed_item.asset, uuid)
        messages.info(request, f"{borrowed_item.asset.name} returned successfully")
        return redirect("borrowed assets", uuid=uuid)


@login_required(login_url=LOGIN_URL)
def getAssetCategoryDetails(request, uuid, category_pk):
    """
    show details of asset category and list of assets under the catregory
    """
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        category = AssetCategory.objects.get(id=category_pk)
        if category:
            context["item_category"] = category
            context["items"] = Asset.getOrgAssetsByCategory(category_pk, uuid)

        return render(
            request,
            "team/category_asset_details.html",
            context=context,
        )
