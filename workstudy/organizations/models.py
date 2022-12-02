import uuid
from django.db import models
from django.utils.translation import gettext_lazy  as _
from accounts.models import Account
# Create your models here.

class Organization(models.Model):
    organisationChoices = {
        ('personal venture','personal venture'),
        ('Small scale','Small scale'),
        ('medium scale','medium scale'),
    }
    organization_uuid = models.UUIDField(_("Organization's ID"),primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Organization name'),blank = True, null =True,max_length = 100)
    scale = models.CharField(_('Scale of organization'),choices =organisationChoices, max_length = 50 )
    supervisor = models.ForeignKey(Account,verbose_name=_("Organization's creater"), on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name  # type: ignore

    def get_owner_details(self):
        return Account.objects.get(account_uuid = self.supervisor)
    
    @staticmethod
    def get_organizations(x):
        return Organization.objects.filter(supervisor = x)