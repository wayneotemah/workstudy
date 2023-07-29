from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from workstudy.globalsettings import LOGIN_URL


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


@login_required(login_url=LOGIN_URL)
def admin_lost_and_found(request):
    """
        get the list of lost and found assets for the supervisor view
    """
    if request.method == "GET":
        return render(request, "admin_user/lost_and_found.html")
    pass
    pass
