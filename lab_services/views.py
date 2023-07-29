from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from workstudy.globalsettings import LOGIN_URL

from lab_services.models import Found_Item

from assets.models import Asset, Borrowed_Asset
from datetime import date

# Create your views here.


def servicedashboard(request):
    if request.method == "GET":
        username = request.session.get("username")
        phone_number = request.session.get("phone_number")
        admission_number = request.session.get("admission_number")

        context = {
            "username": username,
            "phone_number": phone_number,
            "admission_number": admission_number,
        }
        return render(request, "services/dashboard.html", context)

    if request.method == "POST":
        context = {}
        return render(request, "services/dashboard.html", context)


def serviceborrowasset(request):
    """
    get request return the listt of borrowed assets by the user in borrowe asets page
    post craete a new borrow request and mark the asset as borrowed pending approval
    """
    if request.method == "GET":
        # Try to retrieve user details from the session
        username = request.session.get("username")
        phone_number = request.session.get("phone_number")
        admission_number = request.session.get("admission_number")

        requested_asset = Borrowed_Asset.objects.filter(student_id=admission_number)
        print(requested_asset)
        # gets available assets
        available_assets = Asset.getAllAvailableAssets()

        context = {
            "username": username,
            "phone_number": phone_number,
            "admission_number": admission_number,
            "available_assets": available_assets,
        }
        return render(request, "services/borrow_asset.html", context)
    if request.method == "POST":
        # Process the form data here and save the user details in the session
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        admission_number = request.POST.get("admission_number")

        # Save the user details in the session
        request.session["username"] = username
        request.session["phone_number"] = phone_number
        request.session["admission_number"] = admission_number
        request.session.save()  # Save the session explicitly

        # getting user requires data to write to database
        person = request.POST.get("username")
        student_id = request.POST.get("admission_number")
        contacts = request.POST.get("phone_number")
        location_of_use = request.POST.get("location_of_use")
        picked_on = request.POST.get("picked_on")

        # getting the asset
        asset = Asset.objects.get(pk=request.POST.get("borrowed_asset"))

        # adding Pending Asset to BorrowedAsset to Table
        borrowed_asset = Borrowed_Asset(
            asset=asset,
            lab=asset.Lab,
            person=person,
            student_id=student_id,
            contacts=contacts,
            location_of_use=location_of_use,
            time_picked_on=picked_on,
            asset_status="Pending Approval",
            date_picked_on=date.today(),
        )
        borrowed_asset.save()

        # updates the asset status to Pending Approval
        asset.status = "Pending Approval"
        asset.save()

        messages.success(
            request, f"Your request has been made. Go by Lab 1 to pick uo the item"
        )

        context = {
            "username": username,
            "phone_number": phone_number,
            "admission_number": admission_number,
        }

        return render(request, "services/borrow_asset.html", context)


@login_required(login_url=LOGIN_URL)
def admin_lost_and_found(request):
    """
    get the list of lost and found assets for the supervisor view
    """
    if request.method == "GET":
        return render(request, "admin_user/lost_and_found.html")
    pass
    pass


def servicesFoundAsset(request):
    """
    get request return the list of found assets by the user in found assets page
    """
    if request.method == "GET":
        found_items = Found_Item.objects.all()

        # Include the found items data in the template context
        context = {
            "found_items_data": found_items,
        }

        return render(request, "services/Lost_and_found.html", context)
