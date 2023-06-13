from django.urls import path


from . import views

urlpatterns = [
    path("sign-in/", views.sign_in, name="sign in"),
    path("sign-up/", views.sign_up, name="sign up"),
    path("createprofile/", views.createprofile, name="createprofile"),
    path("account/", views.account, name="account"),
    path("Lab/", views.Labview, name="choose Lab"),
    path("create_Lab/", views.create_Lab, name="create Lab"),
    path("schedule/<str:uuid>", views.schedule, name="pick my schedule"),
    path("", views.Labview, name="landing redirect")
    # path('roles/' ,views.roles, name='Lab roles')
]
