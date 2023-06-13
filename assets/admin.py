from django.contrib import admin

# Register your models here.

from .models import Asset, Borrowed_Asset, AssetCategory


class AssetViewAdmin(admin.ModelAdmin):
    pass


class Borrowed_AssetViewAdmin(admin.ModelAdmin):
    pass


class Caretory_AssetViewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Asset, AssetViewAdmin)
admin.site.register(AssetCategory, Caretory_AssetViewAdmin)
admin.site.register(Borrowed_Asset, Borrowed_AssetViewAdmin)
