from django.urls import path

from . import views

urlpatterns = [
    path('<str:uuid>/',views.assets, name ='assets'),
]