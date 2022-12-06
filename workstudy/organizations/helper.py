from organizations.models import Organization
from accounts.models import Account

class UserDetailsHelper():
    def __init__(self,user,uuid) -> None:
        self.user = user
        self.companyUUID = uuid

    def get_nav_details(self)-> dict:
        organizationName  = Organization.objects.get(organization_uuid = self.companyUUID )

        userAccount = Account.get_account(self.user)
        username = " ".join([userAccount.first_name,userAccount.last_name])   # type: ignore

        context = {
            "username":username,
            "organizationName":organizationName,
            "organizationUUID":self.companyUUID
        }
        return context

    
class RolesHelper(UserDetailsHelper):
    def __init__(self,user,uuid):
        super().__init__(user,uuid)
    pass

class TeamsHelper(UserDetailsHelper):
    pass

class ReportsHelper(UserDetailsHelper):
    pass

class AssetsHelper(UserDetailsHelper):
    pass




''''
TODO: create a USERDETAILS superclass with teh get nav details funtionality. Inputes are user,uuid to return 



TODO: create role,team,reports and profile class that inherites from USERDETAILS
'''