from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.servicedashboard,
        name="service dashbaord",
    ),
    path(
        "borrow_asset",
        views.serviceborrowasset,
        name="service borrow asset",
    ),
]
