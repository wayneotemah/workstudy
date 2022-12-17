from django.urls import path

from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign in'),  # type: ignore
    path('sign-up/', views.sign_up, name='sign up'),  # type: ignore
    path('createprofile/',views.createprofile,name = 'createprofile'),  # type: ignore
    path('account/', views.account, name='account'),
    path('organization/', views.organization, name='choose organization'),
    path('create_organization/', views.create_organization, name='create organization'),  # type: ignore
    path('schedule/<str:uuid>', views.schedule, name='pick my schedule'),
    # path('roles/' ,views.roles, name='organization roles')
]
