from django.contrib import admin
from .models import CustomUser,Account

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    # TODO Set up  django site
    pass

class AccountAdmin(admin.ModelAdmin):
    # TODO Set up  django site 
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
