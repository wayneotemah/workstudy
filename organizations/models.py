import uuid
from django.db import models
from django.utils.translation import gettext_lazy  as _
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Organization(models.Model):
    organization_uuid = models.UUIDField(_("Organization's ID"),primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Organization name'),blank = True, null =True,max_length = 100)
    supervisor = models.OneToOneField(Account,verbose_name=_("Organization's creater"), on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name  # type: ignore

    def get_owner_details(self):
        return Account.objects.get(account_uuid = self.supervisor)
    
    @staticmethod
    def get_organizations(x):
        try:
            return Organization.objects.get(supervisor = x)
        except ObjectDoesNotExist as e:
            return None

    @staticmethod
    def get_organizations_from_uuid(x):
        try:
            return Organization.objects.get(organization_uuid = x)
        except ObjectDoesNotExist as e:
            return None


class Issue(models.Model):
    issueStates = {
        ('Done','Done'),
        ('Argent','Argent'),
        ('Pending','Pending'),
        
    }
    organization = models.ForeignKey(Organization, verbose_name=_("organization/lab"), on_delete=models.CASCADE)
    details =models.TextField(verbose_name = _("issue details"), max_length=150)
    reported_on = models.DateTimeField(verbose_name = _("date reported"))
    status = models.CharField(verbose_name = _("state"), max_length=50, choices=issueStates)
    reported_by = models.ForeignKey(Account, verbose_name=_("reported_by"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues")
        ordering = ['-reported_on']

    def __str__(self):
        return f"{self.pk}-{self.reported_on}"

    @staticmethod
    def getList(x):
        #get all organizations issues
        return Issue.objects.filter(organization = x)
        

    @staticmethod
    def getUserList(x):
        """
        get list of issues made by user
        x -> account 
        """
        reporter = Account.get_account(x)
        return Issue.objects.filter(reported_by = reporter)
    
    @staticmethod
    def getListbyStatus(x,y):
        #get all organizations issues
        return Issue.objects.filter(organization = x, status = y)

    @staticmethod
    def getIssueByPk(x):
        return Issue.objects.get(pk = x)

