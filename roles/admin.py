from django.contrib import admin

from roles.models import Role, Task ,UserRole

# Register your models here.

# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    # TODO Set up  django site 
    pass
class TaskAdmin(admin.ModelAdmin):
    # TODO Set up  django site 
    pass

class UserRoleAdmin(admin.ModelAdmin):
    # TODO Set up  django site 
    pass

admin.site.register(UserRole,UserRoleAdmin)

admin.site.register(Role, RoleAdmin)

admin.site.register(Task, TaskAdmin)

