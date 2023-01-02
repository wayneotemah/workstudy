from django.contrib import admin

# Register your models here.

from .models import Asset,Borrowd_Asset

class AssetViewAdmin(admin.ModelAdmin):
    pass
class Borrowd_AssetViewAdmin(admin.ModelAdmin):
    pass

admin.site.register(Asset,AssetViewAdmin)
admin.site.register(Borrowd_Asset,Borrowd_AssetViewAdmin)