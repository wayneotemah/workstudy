from organizations.models import Issue, Organization
from accounts.models import Account, CustomUser
from roles.models import Role, UserRole
from datetime import datetime, timedelta


class UserAdminDetailsHelper:
    def __init__(self, user, uuid) -> None:
        self.user = user
        self.companyUUID = uuid

    def get_nav_details(self) -> dict:
        organizationName = Organization.objects.get(organization_uuid=self.companyUUID)

        userAccount = Account.get_account(self.user)
        username = " ".join([userAccount.first_name, userAccount.last_name])
        # role = UserRole.getUserOrganizationRoles(userAccount).role.title
        context = {
            "username": username,
            "organizationName": organizationName,
            "organizationUUID": self.companyUUID,
            "role": "Supervisor",
        }
        return context

    def get_profile(self) -> dict:
        userinstance = CustomUser.objects.get(pk=self.user.pk)
        email_address = userinstance.get_email_address()
        phone_number = userinstance.get_phone_number()

        organizationName = Organization.objects.get(organization_uuid=self.companyUUID)
        userAccount = Account.get_account(self.user)
        firstname = userAccount.first_name
        lastname = userAccount.last_name
        username = " ".join([firstname, lastname])  # type: ignore
        role = UserRole.getUserOrganizationRoles(userAccount).role.title  # type: ignore

        context = {
            "username": username,
            "organizationName": organizationName,
            "organizationUUID": self.companyUUID,
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
        return UserRole.getUsersInOrganization(self.companyUUID)

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

        role = UserRole.getUserOrganizationRoles(teamMemberAccount).role.title

        # navbar details
        organizationName = Organization.objects.get(organization_uuid=self.companyUUID)
        firstname = teamMemberAccount.first_name
        lastname = teamMemberAccount.last_name
        account_uuid = teamMemberAccount.account_uuid
        username = " ".join([firstname, lastname])

        context = {
            "username": username,
            "organizationName": organizationName,
            "organizationUUID": self.companyUUID,
            "role": role,
            "email_address": email_address,
            "phone_number": phone_number,
            "lastname": lastname,
            "firstname": firstname,
            "is_active": is_active,
            "account_uuid":account_uuid,
        }
        return context


class RolesAdminHelper(UserAdminDetailsHelper):
    def __init__(self, user, uuid):
        super().__init__(user, uuid)

    def get_roles(self):
        data = Role.getOrganizationRoles(self.companyUUID)
        return data


class IssuessAdminHelper(UserAdminDetailsHelper):
    def __init__(self, user, uuid):
        super().__init__(user, uuid)

    def getAllIssuesList(self):
        return Issue.getList(self.companyUUID)

    def getAllUserIssuesList(self):
        return Issue.getUserList(self.user)
