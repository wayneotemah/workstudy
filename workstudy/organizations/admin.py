from django.contrib import admin

from organizations.models import Organization

# Register your models here.

class OrganizationAdmin(admin.ModelAdmin):
    # TODO Set up  django site 
    pass


admin.site.register(Organization, OrganizationAdmin)