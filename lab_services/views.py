from django.shortcuts import render
from lab_services.models import Found_Item

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

        context = {
            "username": username,
            "phone_number": phone_number,
            "admission_number": admission_number,
        }
        return render(request, "services/borrow_asset.html", context)
    if request.method == "POST":
        # Process the form data here and save the user details in the session
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        admission_number = request.POST.get("addmission_number")

        # Save the user details in the session
        request.session["username"] = username
        request.session["phone_number"] = phone_number
        request.session["admission_number"] = admission_number
        request.session.save()  # Save the session explicitly

        context = {
            "username": username,
            "phone_number": phone_number,
            "admission_number": admission_number,
        }

        return render(request, "services/borrow_asset.html", context)


def servicesFeedBack(request):
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
