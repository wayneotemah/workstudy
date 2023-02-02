import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from organizations.models import Organization


def asset_photo_upload(instance, filename):
    """Gives a unique path to the saved photo in models.
    Arguments:
        instance: the photo itself, it is not used in this
                  function but it's required by django.
        filename: the name of the photo sent by user, it's
                  used here to get the format of the file.
    Returns:
        The unique path that the file will be stored in the DB.
    """
    return 'media/assets_imgs/{0}.{1}'.format(uuid.uuid4().hex, os.path.splitext(filename))


def asset_categorty_photo_upload(instance, filename):
    return 'media/asset_category/{0}.{1}'.format(uuid.uuid4().hex, os.path.splitext(filename))


class AssetCategory(models.Model):
    '''
    models for asset category
    '''
    asset_categories = {
        ('Projector', 'Projector'),
        ('VGA Cables', 'VGA Cables'),
        ('HDMI Cables', 'HDMI Cables'),
        ('VGA-HDMI Converters', ' VGA-HDMI Converters'),
        ('Others', 'Others')
    }
    categorty_name = models.TextField(
        _("Asset category name"), choices=asset_categories, max_length=50, null=False, blank=False)
    categoty_pic = models.ImageField(
        _("Category image"), upload_to=asset_categorty_photo_upload, null=False, blank=False)
    quantity = models.PositiveIntegerField(_("number of assets available"))
    woring_quantity = models.PositiveIntegerField(
        _("number is assets that are working"))

    class Meta:
        verbose_name = _("Asset Category")
        verbose_name_plural = _("Asset Categories")

    def __str__(self):
        return self.categorty_name


class Asset(models.Model):
    '''
    model for organisations /  labs assets 
    '''
    asset_status = {
        ('Borrowed', 'Borrowed'),
        ('Available', 'Available'),
        ('Not available', ' Not available')
    }
    asset_condition = {
        ('Good', 'Good'),
        ('Faulty', 'Faulty'),
        ('Not Woking', 'Not Working')
    }
    name = models.CharField(verbose_name="item name", max_length=50)
    category_type = models.ForeignKey(
        AssetCategory, verbose_name=_(""), on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(
        Organization, verbose_name="lab / organization", on_delete=models.CASCADE)
    pic = models.ImageField(
        _(" asset image"), upload_to=asset_photo_upload, null=False)
    status = models.CharField(
        _("asset status"), choices=asset_status, max_length=50)
    condition = models.CharField(
        _("asset condition"), choices=asset_condition, max_length=50)

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

        return Asset.objects.filter(organization=x)

    @staticmethod
    def getSingleAsset(x):
        '''
        get a single  assets 
        '''

        return Asset.objects.get(pk=x)

    @staticmethod
    def getAvailbleAssets(x):
        '''
        get the available assets of organization x
        '''
        return Asset.objects.filter(organization=x, status="Available")


class Borrowd_Asset(models.Model):
    '''
    models for the assets dorrowed
    '''
    asset = models.ForeignKey(
        Asset, verbose_name="borrowed item", on_delete=models.CASCADE)
    organization_id = models.ForeignKey(
        Organization, verbose_name="lab", on_delete=models.CASCADE)
    person = models.CharField(_("borrowers name(one)"),
                              max_length=50, blank=False, null=False)
    contacts = models.CharField(
        _("borrowers contact"), max_length=50, blank=False, null=False)
    location_of_use = models.CharField(
        _("Class/Hall"), max_length=50, blank=False, null=False)
    picked_on = models.DateTimeField(_("date and time picked"), editable=False)
    returned_on = models.DateTimeField(
        _("date and time returned"), blank=True, null=True)
    returned = models.BooleanField()

    class Meta:
        verbose_name = _("Borrowd Asset")
        verbose_name_plural = _("Borrowd Assets")
        ordering = ['returned_on']

    def __str__(self):
        return f'{self.asset}'

    @staticmethod
    def getBorrowedAssets(x):
        '''
        get the assets of organization x, that are borrowed
        '''
        return Borrowd_Asset.objects.filter(organization_id=x)

    @staticmethod
    def getSingleBorrowedAssets(x):
        '''
        get the single borrowed using the records pk
        '''
        return Borrowd_Asset.objects.get(pk=x)

    @staticmethod
    def getAssetByPK(x):
        '''
        returns the lates infomation about an asset by it primary key
        '''
        return Borrowd_Asset.objects.filter(asset=x).last()
