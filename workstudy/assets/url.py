from django.urls import path

from . import views

urlpatterns = [
    path('<str:uuid>/',views.assets, name ='assets'),
    path('add_item/<str:uuid>/',views.post_asset, name ='add asset'),
    path('borrowed_assets/<str:uuid>/',views.borrowed_assets, name ='borrowed assets'),
    path('borrowed_assets_page/<str:uuid>/',views.borrowed_assets_page, name ='borrowedassetspage'),
    path('return_asset/<str:uuid>/<int:borrowedasset_id>',views.return_asset, name ='return assets'),
]