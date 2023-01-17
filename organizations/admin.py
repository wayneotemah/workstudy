from django.contrib import admin

from organizations.models import Organization,Issue

# Register your models here.

class OrganizationAdmin(admin.ModelAdmin):
    # TODO Set up  django site 
    pass

class IssueAdmin(admin.ModelAdmin):
    # TODO Set up  django site 
    pass




admin.site.register(Issue, IssueAdmin)
admin.site.register(Organization, OrganizationAdmin)