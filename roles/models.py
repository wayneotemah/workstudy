from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy  as _
from organizations.models import Organization
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist

from datetime import date, timedelta, datetime
import calendar


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
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thurday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
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
        return Organization.objects.get(organization_uuid = role.role.organization.organization_uuid)
    
    @staticmethod
    def check_user_schedule(x):
        role = UserRole.getUserOrganizationRoles(x)
        if role:
            if not role.day1 and not role.day2 and not role.day3 and not role.day4 and not role.day5 and not role.day6 :
                return None
            else:
                return True
        elif role == None:
            return False
            
    @staticmethod
    def getUserSchedule(x):
        role = UserRole.objects.get(assigned_to = x)
        data = []
        if role.day1:
            data.append({
                "day":role.day1,
                "start_time":role.day1_start_time,
                "end_time":role.day1_end_time, 
            })

        if role.day2:
            data.append({
                "day":role.day2,
                "start_time":role.day2_start_time,
                "end_time":role.day2_end_time, 
            })

        if role.day3:
            data.append({
                "day":role.day3,
                "start_time":role.day3_start_time,
                "end_time":role.day3_end_time, 
            })

        if role.day4:
            data.append({
                "day":role.day4,
                "start_time":role.day4_start_time,
                "end_time":role.day4_end_time, 
            })

        if role.day5:
            data.append({
                "day":role.day5,
                "start_time":role.day5_start_time,
                "end_time":role.day5_end_time, 
            })

        if role.day6:
            data.append({
                "day":role.day6,
                "start_time":role.day6_start_time,
                "end_time":role.day6_end_time, 
            })
        return data

    @staticmethod
    def addToSchelule(account,day,start_time,end_time):
        role = UserRole.objects.get(assigned_to = account)
        if role.day1 == None:
            role.day1 = day
            role.day1_start_time = start_time
            role.day1_end_time = end_time
            role.save()
            return True

        elif role.day2 == None:
            role.day2 = day
            role.day2_start_time = start_time
            role.day2_end_time = end_time
            role.save()
            return True

        elif role.day3 == None:
            role.day3 = day
            role.day3_start_time = start_time
            role.day3_end_time = end_time
            role.save()
            return True

        elif role.day4 == None:
            role.day4 = day
            role.day4_start_time = start_time
            role.day4_end_time = end_time
            role.save()
            return True

        elif role.day5 == None:
            role.day5 = day
            role.day5_start_time = start_time
            role.day5_end_time = end_time
            role.save()
            return True

        elif role.day6 == None:
            role.day6 = day
            role.day6_start_time = start_time
            role.day6_end_time = end_time
            role.save()
            return True

        else:
            return False

    @staticmethod
    def getLatestSchedule(x):
        """
        get the next closesed schedule from today for the
        returns day, start time and end time of the schedule
        """
        
        role = UserRole.objects.get(assigned_to = x)        
        day = date.today()
        counter = 0
        curr_date = day.weekday()
        
        while counter <= 6:
            new_date = curr_date + counter # current day + counter 
            new_date = new_date % 6 # mod to get the day of the week
            day_today = (calendar.day_name[new_date])
            print(day_today,new_date)
            data = []

            if role.day1 == day_today:
                data.append({
                    "day":role.day1,
                    "start_time":role.day1_start_time,
                    "end_time":role.day1_end_time, 
                })
                return data

            elif role.day2 == day_today:
                data.append({
                    "day":role.day2,
                    "start_time":role.day2_start_time,
                    "end_time":role.day2_end_time, 
                })
                return data

            elif role.day3 == day_today:
                data.append({
                    "day":role.day3,
                    "start_time":role.day3_start_time,
                    "end_time":role.day3_end_time, 
                })
                return data
                
            elif role.day4 == day_today:
                data.append({
                    "day":role.day4,
                    "start_time":role.day4_start_time,
                    "end_time":role.day4_end_time, 
                })
                return data

            elif role.day5 == day_today:
                data.append({
                    "day":role.day5,
                    "start_time":role.day5_start_time,
                    "end_time":role.day5_end_time, 
                })
                return data

            elif role.day6 == day_today:
                data.append({
                    "day":role.day6,
                    "start_time":role.day6_start_time,
                    "end_time":role.day6_end_time, 
                })
                return data
            
            print(f' count  {counter}')
            counter +=1 # increment counter



        

# def checksixHrrang(x):
#     now = datetime.now()
#     current_time = now.strftime("%H:%M")
#     event_time = x
#     event_time = datetime.combine(datetime.today(), event_time)


#     # Check if the current time is within 30 minutes of the other time
#     if (now - timedelta(minutes=30) <= event_time <= now + timedelta(hours=6)):
#         print("The current time is within 30 minutes of the other time.")
#     else:
#         print("The current time is not within 30 minutes of the other time.")
#     print(current_time)

#     print(now) # type: ignore
#     print(event_time) # type: ignore
#     pass

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