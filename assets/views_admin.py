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


@login_required(login_url=LOGIN_URL)
def admin_assets_catrgory(request, uuid):
    # get all assets for the organisation/lab
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
        return render(request, "admin_user/categoryassets.html", context=context)
    elif request.method == "POST":
        category = request.POST["category_type"]
        pic = request.FILES["asset_category_pic"]
        try:
            categoryItem = AssetCategory(
                category=category, category_pic=pic, organization_id=uuid
            )
            categoryItem.save()
            messages.success(request, f"Added new catrogy of asset 👍")
            return redirect(admin_assets_catrgory, uuid=uuid)

        except IntegrityError as e:
            messages.warning(request, e)
            return render(request, "errorpage.html", context=context)

        except Exception as e:
            # if anything fails, show error page wtth message
            context = {
                "message": f"Please contact the devs and notify them of the error \nerror is: \n{e}"
            }
            messages.warning(request, "Unexpected Exception error has risen")
            return render(request, "errorpage.html", context=context)


@login_required(login_url=LOGIN_URL)
def admin_postassetCategory(request, uuid):
    """
    returns page with post asset form
    """
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        return render(request, "admin_user/addassetcategory.html", context=context)
    


# @login_required(login_url=LOGIN_URL)
# def admin_assetDetails(request, uuid, item_pk):
#     """
#     show detils assets
#     """
#     if request.method == "GET":
#         helper = AssetsHelper(user=request.user, uuid=uuid)
#         context = helper.get_nav_details()
#         item = helper.getAssetDetails(item_pk)
#         if item.status == "Borrowed":
#             item_borrowed_details = Borrowd_Asset.objects.get(asset=item)
#             context["item"] = item
#             context["borrowed_item"] = item_borrowed_details
#         else:
#             context["item"] = item

#         return render(request, "admin_user/item_asset_details.html", context=context)


@login_required(login_url=LOGIN_URL)
def admin_assetDetails(request, uuid, category_pk):
    """
    show details of asset category and list of assets under the catregory
    """
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        category = AssetCategory.getCategory(category_pk, uuid)
        if category:
            context["item_category"] = category
            context["items"] = Asset.getOrgAssetsByCategory(category_pk, uuid)

            return render(request, "admin_user/category_asset_details.html", context=context)
        

@login_required(login_url=LOGIN_URL)
def admin_post_asset(request, uuid, category_pk):
    # get asset posting page
    if request.method == "GET":
        helper = AssetsHelper(user=request.user, uuid=uuid)
        context = helper.get_nav_details()
        context["category_pk"] = category_pk
        context['category'] = AssetCategory.objects.get(id = category_pk)
        return render(request, "admin_user/addasset.html", context=context)
    if request.method == "POST":
        # adding asset
        now = datetime.datetime.now()

        name = request.POST["asset_name"]
        condition = request.POST["condition"]
        status = request.POST["status"]
        pic = request.FILES["asset_pic"]
        try:
            # try to save
            # category = AssetCategory.getCategoryByName(
            #     category_type)  # get the asset instance
            # organization = Organization.get_organizations_from_uuid(
            #     uuid)  # get organization instance for saving
            asset = Asset(
                category_type_id=category_pk,
                name=name,
                condition=condition,
                status=status,
                pic=pic,
                organization_id=uuid,
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
            return redirect(admin_post_asset, uuid=uuid, category_pk=category_pk)