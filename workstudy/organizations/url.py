from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='admin dasboard'),
    path('assets/',views.assets, name ='organization assets')
]