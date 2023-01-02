from django.shortcuts import render
from assets.helper import AssetsHelper
from django.contrib.auth.decorators import login_required

from workstudy.globalsettings import LOGIN_URL

# Create your views here.

@login_required(login_url=LOGIN_URL)  # type: ignore
def assets(request,uuid):
    helper = AssetsHelper(user = request.user,uuid = uuid )
    context = helper.get_nav_details()
    context['assets'] = helper.getAssets()
    return render(request,"assets.html",context=context)
