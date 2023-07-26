from django.urls import path


from . import views

urlpatterns = [

    path("createprofile/", views.createprofile, name="createprofile"),
    path("account/", views.account, name="account"),
    path("Lab/", views.Labview, name="choose Lab"),
    path("schedule/<str:uuid>", views.schedule, name="pick my schedule"),
    path("", views.Labview, name="landing redirect")
]
