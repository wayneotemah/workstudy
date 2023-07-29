from django.shortcuts import render

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

        # gets available assets
        available_assets = Asset.getAllAvailableAssets()

        context = {
            "username": username,
            "phone_number": phone_number,
            "admission_number": admission_number,
            "available_assets": available_assets
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
            date_picked_on=date.today()
        )
        borrowed_asset.save()
        
        # updates the asset status to Pending Approval
        asset.status = "Pending Approval"
        asset.save()

        context = {
            "username": username,
            "phone_number": phone_number,
            "admission_number": admission_number,
        }

        return render(request, "services/borrow_asset.html", context)


def servicesFeedBack(request):
    pass
