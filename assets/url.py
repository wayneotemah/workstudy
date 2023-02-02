from django.urls import path

from . import views

urlpatterns = [
    path('<str:uuid>/', views.assetCategory, name='category assets'),
    path('add_item/<str:uuid>/', views.post_asset, name='add asset'),
    path('borrowed_assets/<str:uuid>/',
         views.borrowed_assets, name='borrowed assets'),
    path('borrowed_assets_page/<str:uuid>/',
         views.borrowed_assets_page, name='borrowedassetspage'),
    path('add_category/<str:uuid>/',
         views.postassetCategory, name='add asset category'),
    path('category/<str:uuid>/<int:cat_id>',
         views.categoryDetails, name='category'),
    path('details/<str:uuid>/<int:asset_pk>',
         views.getAssetDetails, name='asset details'),
    path('return_asset/<str:uuid>/<int:borrowedasset_id>',
         views.return_asset, name='return assets'),
]
