from django.urls import path

from . import views, views_admin




admin_urls = [
    path('admin/<str:uuid>/', views_admin.admin_assets_catrgory, name='admin assets'),
    path('admin/addcategory/<str:uuid>/', views_admin.admin_postassetCategory, name='admin post assets'),
    path('admin/category_details/<str:uuid>/<int:category_pk>/', views_admin.admin_category_Details, name='admin assets details'),
    path('admin/add_asset/<str:uuid>/<int:category_pk>/', views_admin.admin_post_asset, name='admin add assets'),
    path('admin/borrowed_assets/<str:uuid>/', views_admin.admin_borrowed_assets, name='admin borrow asset'),
    path('admin/add_borrowed_asset/<str:uuid>/', views_admin.admin_borrowed_assets_page, name='admin add borrow asset'),
    path('admin/borrowed_asset_details/<str:uuid>/<str:item_pk>/', views_admin.admin_assetDetails, name='admin borrowed asset details'),
    path('admin/return_asset/<str:uuid>/<int:borrowedasset_id>/', views_admin.admin_return_asset, name='admin return asset'),
    
]

urlpatterns = [
    path('<str:uuid>/', views.assetCategory, name='category assets'),

    path('add_item/<str:uuid>/<str:category_pk>', views.post_asset, name='add asset'),

    path('borrowed_assets/<str:uuid>/',
         views.borrowed_assets, name='borrowed assets'),

    path('borrowed_assets_page/<str:uuid>/',
         views.borrowed_assets_page, name='borrowedassetspage'),

    path('add_category/<str:uuid>/',
         views.postassetCategory, name='add asset category'),

    path('category_details/<str:uuid>/<int:category_pk>/',
         views.getAssetCategoryDetails, name='asset category details'),

    path('return_asset/<str:uuid>/<int:borrowedasset_id>/',
         views.return_asset, name='return assets'),

    path('assets_details/<str:uuid>/<str:item_pk>/',
         views.assetDetails, name="asset details"),
] + admin_urls
