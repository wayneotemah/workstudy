from django.urls import path

from . import views

urlpatterns = [
    path('', views.sign_in, name='sign in'),  # type: ignore
    path('sign-up/', views.sign_up, name='sign up'),  # type: ignore
    path('createprofile/',views.createprofile,name = 'createprofile'),
    path('account/', views.account, name='account'),
    path('organization/', views.organization, name='choose organization'),
    path('create_organization/', views.create_organization, name='create organization'),
    path('schedule/', views.schedule, name='pick my schedule'),
]