from organizations.models import Issue, Organization
from accounts.models import Account, CustomUser
from roles.models import Role, UserRole
from datetime import datetime, timedelta

class UserDetailsHelper():
    def __init__(self,user,uuid) -> None:
        self.user = user
        self.companyUUID = uuid

    def get_nav_details(self)-> dict:
        organizationName  = Organization.objects.get(organization_uuid = self.companyUUID )

        userAccount = Account.get_account(self.user)
        username = " ".join([userAccount.first_name,userAccount.last_name])   # type: ignore
        role = UserRole.getUserOrganizationRoles(userAccount).role.title # type: ignore

        context = {
            "username":username,
            "organizationName":organizationName,
            "organizationUUID":self.companyUUID,
            "role": role,
        }
        return context


    def get_profile(self):
        userinstance= CustomUser.objects.get(pk = self.user.pk)
        email_address = userinstance.get_email_address()
        phone_number = userinstance.get_phone_number()

        organizationName  = Organization.objects.get(organization_uuid = self.companyUUID )
        userAccount = Account.get_account(self.user)
        firstname = userAccount.first_name
        lastname = userAccount.last_name
        username = " ".join([firstname, lastname])   # type: ignore
        role = UserRole.getUserOrganizationRoles(userAccount).role.title # type: ignore

        context = {
            "username":username,
            "organizationName":organizationName,
            "organizationUUID":self.companyUUID,
            "role": role,
            "email_address":email_address,
            "phone_number":phone_number,
            "lastname":lastname,
            "firstname":firstname

        }
        print(context)
        return context
     

class DashBoardHelper(UserDetailsHelper):
    def __init__(self,user,uuid):
        super().__init__(user,uuid)

    
    def latestSchdule(self):
        userAccount = Account.get_account(self.user)
        data = UserRole.getLatestSchedule(userAccount)

        # now = datetime.now()
        # current_time = now.strftime("%H:%M")
        # event_time = data[0]['end_time']
        # event_time = datetime.combine(datetime.today(), event_time)


        # # Check if the current time is within 30 minutes of the other time
        # if (now - timedelta(minutes=30) <= event_time <= now + timedelta(minutes=30)):
        #     print("The current time is within 30 minutes of the other time.")
        # else:
        #     print("The current time is not within 30 minutes of the other time.")
        # print(current_time)

        # print(now) # type: ignore
        # print(event_time) # type: ignore

        return  data
    
class RolesHelper(UserDetailsHelper):
    def __init__(self,user,uuid):
        super().__init__(user,uuid)

    def get_roles(self):
        data = Role.getOrganizationRoles(self.companyUUID)
        return data

class TeamsHelper(UserDetailsHelper):
    def __init__(self,user,uuid):
        super().__init__(user,uuid)

    def get_members(self):
        user = Account.get_account(self.user)
        data = UserRole.getTeam(UserRole.getUserOrganizationRoles(user).role) # type : ignore 
        return data

class ReportsHelper(UserDetailsHelper):
    pass

class AssetsHelper(UserDetailsHelper):
    def __init__(self,user,uuid):
        super().__init__(user,uuid)


    def getAllIssuesList(self):
        return Issue.getList(self.companyUUID)





''''
TODO: create a USERDETAILS superclass with teh get nav details funtionality. Inputes are user,uuid to return 



TODO: create role,team,reports and profile class that inherites from USERDETAILS
'''