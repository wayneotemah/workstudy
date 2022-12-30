import uuid
from django.db import models
from django.utils.translation import gettext_lazy  as _
from accounts.models import Account
from django.core.exceptions import ObjectDoesNotExist

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