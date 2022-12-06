from django.urls import path

from . import views

urlpatterns = [
    path('<str:uuid>/' ,views.dashboard, name='dashboard'),
    path('redirect/dashboard',views.dashboard_redirect, name= "dashboard redirect"),
    path('assets/',views.assets, name ='organization assets'),

]