from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.


def servicedashboard(request):
    if request.method == "GET":
        context = {}
        context["name"] = request.COOKIES.get("name", "")
        context["phone_number"] = request.COOKIES.get("phone_number", "")
        context["admission_number"] = request.COOKIES.get("admission_number", "")
        return render(request, "services/dashboard.html", context)

    if request.method == "POST":
        context = {}
        if request.POST.get("remeber_me"):
            template = loader.get_template("services/dashboard.html")
            context["name"] = request.POST.get("name")
            context["phone_number"] = request.POST.get("phone_number")
            context["admission_number"] = request.POST.get("admission_number")
            response = HttpResponse(template.render(context, request))
            response.set_cookie(
                "username",
                request.POST.get("username"),
                max_age=604800,
            )
            response.set_cookie(
                "phone_number",
                request.POST.get("phone_number"),
                max_age=604800,
            )
            response.set_cookie(
                "admission_number",
                request.POST.get("admission_number"),
                max_age=604800,
            )
            return response
