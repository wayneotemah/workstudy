from django.db import models
from django.utils.translation import gettext_lazy  as _
from organizations.models import Organization

# Create your models here.


class Role(models.Model):

    title = models.CharField(_('Title'),blank = True, null =True,max_length = 100)
    description = models.TextField(_("role description"),blank = True, null =True,max_length = 100)
    organization = models.ForeignKey(Organization, verbose_name=_("Organization"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.title

    

class Task(models.Model):

    role = models.ForeignKey(Role, verbose_name=_("Role"), on_delete=models.CASCADE)
    task_1 = models.TextField(_("task 1"),blank = True, null =True,max_length = 100)
    task_2 = models.TextField(_("task 2"),blank = True, null =True,max_length = 100)
    task_3 = models.TextField(_("task 3"),blank = True, null =True,max_length = 100)
    task_4 = models.TextField(_("task 4"),blank = True, null =True,max_length = 100)
    task_5 = models.TextField(_("task 5"),blank = True, null =True,max_length = 100)
    task_6 = models.TextField(_("task 6"),blank = True, null =True,max_length = 100)
    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def __str__(self):
        return self.role.title