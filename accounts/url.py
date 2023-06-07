from django.urls import path


from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign in'),
    path('sign-up/', views.sign_up, name='sign up'),
    path('createprofile/', views.createprofile, name='createprofile'),
    path('account/', views.account, name='account'),
    path('organization/', views.organization, name='choose organization'),
    path('create_organization/', views.create_organization,
         name='create organization'),
    path('schedule/<str:uuid>', views.schedule, name='pick my schedule'),
    path('', views.organization, name="landing redirect")
    # path('roles/' ,views.roles, name='organization roles')
]
