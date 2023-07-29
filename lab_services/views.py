from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.


def servicedashboard(request):
    if request.method == "GET":
        context = {}
        context["name"] = request.COOKIES.get("name", "")
        context["phone_number"] = request.COOKIES.get("phone_number", "")
        context["admission_number"] = request.COOKIES.get(
            "admission_number",
            "",
        )
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
        context = {}
        return render(request, "services/borrow_asset.html", context)
