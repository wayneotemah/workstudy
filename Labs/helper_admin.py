from Labs.models import Issue, Lab
from accounts.models import Account, CustomUser
from roles.models import Role, UserRole


class UserAdminDetailsHelper:
    def __init__(self, user, uuid) -> None:
        self.user = user
        self.companyUUID = uuid

    def get_profile(self) -> dict:
        userinstance = CustomUser.objects.get(pk=self.user.pk)
        email_address = userinstance.get_email_address()
        phone_number = userinstance.get_phone_number()

        LabName = Lab.objects.get(Lab_uuid=self.companyUUID)
        userAccount = Account.get_account(self.user)
        firstname = userAccount.first_name
        lastname = userAccount.last_name
        username = " ".join([firstname, lastname])
        try:
            role = UserRole.getUserLabRoles(userAccount).role.title
        except AttributeError:
            role = "Admin"

        context = {
            "username": username,
            "LabName": LabName,
            "LabUUID": self.companyUUID,
            "role": role,
            "email_address": email_address,
            "phone_number": phone_number,
            "lastname": lastname,
            "firstname": firstname,
        }
        return context


class TeamAdminHelper(UserAdminDetailsHelper):
    def __init__(self, user, uuid, account_uuid=None) -> None:
        super().__init__(user, uuid)
        self.account_uuid = account_uuid

    def get_members(self):
        return UserRole.getUsersInLab(self.companyUUID)

    def get_member_profile(self):
        """
        gets the team members profile details from the relevant tables,
        it also returns admin pannel nav bar details
        """
        # team member details
        userinstance = CustomUser.objects.get(account=self.account_uuid)
        teamMemberAccount = Account.objects.get(account_uuid=self.account_uuid)
        email_address = userinstance.get_email_address()
        phone_number = userinstance.get_phone_number()
        is_active = userinstance.is_active

        role = UserRole.getUserLabRoles(teamMemberAccount).role.title

        # navbar details
        LabName = Lab.objects.get(Lab_uuid=self.companyUUID)
        firstname = teamMemberAccount.first_name
        lastname = teamMemberAccount.last_name
        account_uuid = teamMemberAccount.account_uuid
        username = " ".join([firstname, lastname])

        context = {
            "username": username,
            "LabName": LabName,
            "LabUUID": self.companyUUID,
            "role": role,
            "email_address": email_address,
            "phone_number": phone_number,
            "lastname": lastname,
            "firstname": firstname,
            "is_active": is_active,
            "account_uuid": account_uuid,
        }
        return context

    def get_unassigned_user(self):
        return Account.objects.filter(UserRole=None)

        pass


class RolesAdminHelper(UserAdminDetailsHelper):
    def __init__(self, user, uuid):
        super().__init__(user, uuid)

    def get_roles(self):
        data = Role.getLabRoles(self.companyUUID)
        return data


class IssuessAdminHelper(UserAdminDetailsHelper):
    def __init__(self, user, uuid):
        super().__init__(user, uuid)

    def getAllIssuesList(self):
        return Issue.getList(self.companyUUID)

    def getAllUserIssuesList(self):
        return Issue.getUserList(self.user)
