import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
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
    return "media/assets_imgs/{0}.{1}".format(
        uuid.uuid4().hex, os.path.splitext(filename)
    )


def asset_categorty_photo_upload(instance, filename):
    return "media/asset_category/{0}.{1}".format(
        uuid.uuid4().hex, os.path.splitext(filename)
    )


class AssetCategory(models.Model):
    """
    models for asset category
    """

    asset_categories = {
        ("Projector", "Projector"),
        ("VGA Cables", "VGA Cables"),
        ("HDMI Cables", "HDMI Cables"),
        ("VGA-HDMI Converters", " VGA-HDMI Converters"),
        ("Others", "Others"),
    }
    category = models.TextField(
        _("Asset category name"),
        choices=asset_categories,
        max_length=50,
        null=False,
        blank=False,
    )

    category_pic = (
        models.ImageField(
            _("Category image"),
            upload_to=asset_categorty_photo_upload,
            null=True,
            blank=True,
        ),
    )

    quantity = models.PositiveIntegerField(_("number of assets available"), default=0)
    working_quantity = models.PositiveIntegerField(
        _("number is assets that are working"), default=0
    )
    borrowed_assets = models.PositiveIntegerField(
        _("number is assets that are borrowedd"), default=0
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name="lab / organization",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Asset Category")
        verbose_name_plural = _("Asset Categories")

    def __str__(self):
        return f"{self.category}"

    @staticmethod
    def getCategory(x, y):
        """
        get asset category to get instance
        x -> asset category name ie must be in asset_categories choices
        y -> asset organization/lab
        """
        return AssetCategory.objects.get(id=x, organization_id=y)

    @staticmethod
    def getCategoryListByOrganization(x):
        """
        x -> organization/lab uuid
        Use lab/org uuid to get list of all categories in that lab
        """
        return AssetCategory.objects.filter(organization=x)


class Asset(models.Model):
    """
    model for organisations /  labs assets
    """

    asset_status = {
        ("Borrowed", "Borrowed"),
        ("Available", "Available"),
        ("Not available", " Not available"),
    }
    asset_condition = {
        ("Good", "Good"),
        ("Faulty", "Faulty"),
        ("Not Woking", "Not Working"),
    }
    name = models.CharField(verbose_name="item name", max_length=50)
    category_type = models.ForeignKey(
        AssetCategory,
        verbose_name="asset type",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    organization = models.ForeignKey(
        Organization, verbose_name="lab / organization", on_delete=models.CASCADE
    )
    pic = models.ImageField(_(" asset image"), upload_to=asset_photo_upload, null=False)
    status = models.CharField(_("asset status"), choices=asset_status, max_length=50)
    condition = models.CharField(
        _("asset condition"), choices=asset_condition, max_length=50
    )

    class Meta:
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def getAssets(x):
        """
        get the assets of organization x
        """
        return Asset.objects.filter(organization=x)

    @staticmethod
    def getSingleAsset(x):
        """
        get a single  assets
        x = item primary key
        """
        return Asset.objects.get(pk=x)

    @staticmethod
    def getOrgAssetsByCategory(x, y):
        """
        get list of objects by category type and organization ID
        x-> category item id
        y -> org id
        """
        return Asset.objects.filter(category_type_id=x, organization_id=y)

    @staticmethod
    def getAvailbleAssets(x):
        """
        get the available assets of organization x
        """
        return Asset.objects.filter(organization=x, status="Available")


class Borrowd_Asset(models.Model):
    """
    models for the assets dorrowed
    """

    asset = models.ForeignKey(
        Asset, verbose_name="borrowed item", on_delete=models.CASCADE
    )
    organization_id = models.ForeignKey(
        Organization, verbose_name="lab", on_delete=models.CASCADE
    )
    person = models.CharField(
        _("borrowers name(one)"), max_length=50, blank=False, null=False
    )
    contacts = models.CharField(
        _("borrowers contact"), max_length=50, blank=False, null=False
    )
    location_of_use = models.CharField(
        _("Class/Hall"), max_length=50, blank=False, null=False
    )
    picked_on = models.DateTimeField(_("date and time picked"), editable=False)
    returned_on = models.DateTimeField(
        _("date and time returned"), blank=True, null=True
    )
    returned = models.BooleanField()

    class Meta:
        verbose_name = _("Borrowd Asset")
        verbose_name_plural = _("Borrowd Assets")
        ordering = ["returned_on"]

    def __str__(self):
        return f"{self.asset}"

    @staticmethod
    def getBorrowedAssets(x):
        """
        get the assets of organization x, that are borrowed
        """
        return Borrowd_Asset.objects.filter(organization_id=x)

    @staticmethod
    def getSingleBorrowedAssets(x):
        """
        get the single borrowed using the records pk
        """
        return Borrowd_Asset.objects.get(pk=x)

    @staticmethod
    def getAssetByPK(x):
        """
        returns the lates infomation about an asset by it primary key
        """
        return Borrowd_Asset.objects.filter(asset=x).last()


# Post save functioins
# Assets Post save
def asset_count(instance):
    count = Asset.objects.filter(
        category_type=instance.category_type, organization=instance.organization
    )
    count = len(count)

    Category = AssetCategory.getCategory(
        instance.category_type.id, instance.organization.organization_uuid
    )
    Category.quantity = count
    Category.save()


# @receiver(post_save, sender=Asset)
# def updateAssentQuantityOnSave(sender, instance, **kwargs):
#     # count the number of assets with the same category and store in the category_asset quantity
#     asset_count(instance)


# @receiver(post_delete, sender=Asset)
# def updateAssentQuantityOnDelete(sender, instance, **kwargs):
#     asset_count(instance)


# borrowd assets post save
# @receiver(post_save, sender=Borrowd_Asset)
# def updateAssentBorrowed(sender, instance, **kwargs):
#     instance_type = instance.asset.category_type
#     lab = instance.asset.organization
#     status = instance.asset.status
#     print(instance_type,lab,status)
#     count = Asset.objects.filter(category_type = instance_type,organization = lab,status =status)
#     count = len(count)
#     Category = AssetCategory.getCategory(
#         instance.category_type.id, instance.organization.organization_uuid)

#     if instance.asset.status == 'Borrowed':
#         Category.borrowed_assets = count
#         Category.save()
