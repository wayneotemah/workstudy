from django.contrib import admin

from Labs.models import Lab, Issue

# Register your models here.


class LabAdmin(admin.ModelAdmin):
    # TODO Set up  django site
    pass


class IssueAdmin(admin.ModelAdmin):
    # TODO Set up  django site
    pass


admin.site.register(Issue, IssueAdmin)
admin.site.register(Lab, LabAdmin)
