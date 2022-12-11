from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy  as _
from organizations.models import Organization
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.


class Role(models.Model):

    title = models.CharField(_('Title'),blank = True, null =True,max_length = 100)
    description = models.TextField(_("role description"),blank = True, null =True,max_length = 250)
    organization = models.ForeignKey(Organization, verbose_name=_("Organization"), on_delete=models.CASCADE)
    task_1 = models.CharField(_("task 1"),blank = True, null =True,max_length = 200)
    task_2 = models.CharField(_("task 2"),blank = True, null =True,max_length = 200)
    task_3 = models.CharField(_("task 3"),blank = True, null =True,max_length = 200)
    task_4 = models.CharField(_("task 4"),blank = True, null =True,max_length = 200)
    task_5 = models.CharField(_("task 5"),blank = True, null =True,max_length = 200)
    task_6 = models.CharField(_("task 6"),blank = True, null =True,max_length = 200)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.title

    @staticmethod
    def getOrganizationRoles(x):
        return Role.objects.filter(organization = x)


class UserRole(models.Model):
    days_option = {
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thurday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    }
    role = models.ForeignKey(Role, verbose_name=_("role"), on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Account, verbose_name=_("assigned_to"), on_delete=models.DO_NOTHING,blank = True, null =True)
    
    day1 = models.CharField(max_length=15,choices=days_option,blank = True, null =True)
    day1_start_time = models.TimeField(blank = True, null =True)
    day1_end_time = models.TimeField(blank = True, null =True)
    day2 = models.CharField(max_length=15,choices=days_option,blank = True, null =True)
    day2_start_time = models.TimeField(blank = True, null =True)
    day2_end_time = models.TimeField(blank = True, null =True)
    day3 = models.CharField(max_length=15,choices=days_option,blank = True, null =True)
    day3_start_time = models.TimeField(blank = True, null =True)
    day3_end_time = models.TimeField(blank = True, null =True)
    day4 = models.CharField(max_length=15,choices=days_option,blank = True, null =True)
    day4_start_time = models.TimeField(blank = True, null =True)
    day4_end_time = models.TimeField(blank = True, null =True)
    day5 = models.CharField(max_length=15,choices=days_option,blank = True, null =True)
    day5_start_time = models.TimeField(blank = True, null =True)
    day5_end_time = models.TimeField(blank = True, null =True)
    day6 = models.CharField(max_length=15,choices=days_option,blank = True, null =True)
    day6_start_time = models.TimeField(blank = True, null =True)
    day6_end_time = models.TimeField(blank = True, null =True)

    class Meta:
        verbose_name = _("User's role")
        verbose_name_plural = _("User's  roles")

    def __str__(self):
        return f'{self.assigned_to.first_name} {self.assigned_to.last_name}' # type: ignore

    @staticmethod
    def getUserOrganizationRoles(x):
        try:
            return UserRole.objects.get(assigned_to = x)
        except ObjectDoesNotExist as e:
            return None 

    @staticmethod
    def getTeam(x):
        return UserRole.objects.filter(role = x)

    @staticmethod
    def getOrganization(x):
        role = UserRole.objects.get(assigned_to = x)
        return Organization.objects.filter(organization_uuid = role.role.organization.organization_uuid)
    
    @staticmethod
    def check_user_schedule(x):
        role = UserRole.getUserOrganizationRoles(x)
        if role:
            if not role.day1 and not role.day2 and not role.day3 and not role.day4 and not role.day5 and not role.day6 :
                return None
            else:

                return True
        elif role == None:
            print('check 4')

            return False




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