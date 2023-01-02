from django.urls import path

from . import views

urlpatterns = [
    path('<str:uuid>/',views.assets, name ='assets'),
    path('add_item/<str:uuid>/',views.assets, name ='add asset'),
]