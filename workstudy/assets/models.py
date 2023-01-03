import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy  as _

from organizations.models import Organization

def photo_upload(instance, filename):
    """Gives a unique path to the saved photo in models.
    Arguments:
        instance: the photo itself, it is not used in this
                  function but it's required by django.
        filename: the name of the photo sent by user, it's
                  used here to get the format of the file.
    Returns:
        The unique path that the file will be stored in the DB.
    """

    return 'users/{0}.{1}'.format(uuid.uuid4().hex, os.path.splitext(filename))

class Asset(models.Model):
    '''
    model for organisations /  labs assets 
    '''
    asset_status = {
        ('Borrowed' , 'Borrowed'),
        ('Available' , 'Available'),
        ('Not available' , ' Not available')
    }
    asset_condition= {
        ('Good','Good'),
        ('Faulty','Faulty'),
        ('Not Woking' , 'Not Working')
    }
    name = models.CharField(verbose_name = "item name", max_length=50)
    organization = models.ForeignKey(Organization, verbose_name="lab / organization", on_delete=models.CASCADE)
    pic = models.ImageField(_(" asset image"), upload_to=photo_upload, null=False)
    status = models.CharField(_("asset status"),choices=asset_status, max_length=50)
    condition = models.CharField(_("asset condition"),choices=asset_condition, max_length=50)

    
    class Meta:
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")

    def __str__(self):
        return f'{self.name}'

    @staticmethod
    def getAssets(x):
        '''
        get the assets of organization x
        '''

        return Asset.objects.filter(organization = x)


class Borrowd_Asset(models.Model):
    '''
    models for the assets dorrowed
    '''
    name = models.OneToOneField(Asset, verbose_name="borrowed item", on_delete=models.CASCADE)
    persion = models.CharField(_("borrowers name(one)"), max_length=50,blank=False,null=False)
    email = models.CharField(_("borrowers contact"), max_length=50,blank=False,null=False)
    location_of_use = models.CharField(_("Class/Hall"), max_length=50,blank=False,null=False)
    picked_on = models.DateTimeField(_("date and time picked"), auto_now=True, editable=False)
    returned_on = models.DateTimeField(_("date and time returned"),blank=True,null=True, editable=False)
    returned  = models.BooleanField()
  

    class Meta:
        verbose_name = _("Borrowd Asset")
        verbose_name_plural = _("Borrowd Assets")

    def __str__(self):
        return f'{self.name}'
