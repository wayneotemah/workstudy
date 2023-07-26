import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from Labs.models import Lab

from accounts.models import Account


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
        ("Remote", "Remote"),
        ("Extension/Power Cables", "Extension/Power Cables"),
        ("Others", "Others"),
    }
    category = models.TextField(
        _("Asset category name"),
        choices=asset_categories,
        max_length=50,
        null=False,
        blank=False,
    )

    category_pic = models.ImageField(
        _("Category image"),
        upload_to=asset_categorty_photo_upload,
        null=True,
        blank=True,
    )

    quantity = models.PositiveIntegerField(
        _("number of assets available"),
        default=0,
    )
    working_quantity = models.PositiveIntegerField(
        _("number is assets that are working"), default=0
    )
    borrowed_assets = models.PositiveIntegerField(
        _("number is assets that are borrowedd"), default=0
    )
    Lab = models.ForeignKey(
        Lab,
        verbose_name="lab",
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
        y -> asset Lab/lab
        """
        return AssetCategory.objects.get(category=x, Lab_id=y)

    @staticmethod
    def getCategoryListByLab(x):
        """
        x -> Lab/lab uuid
        Use lab/org uuid to get list of all categories in that lab
        """
        return AssetCategory.objects.filter(Lab=x).order_by("id")

    @staticmethod
    def add_borrowed_assets(asset, uuid):
        """
        asset -> asset category instance
        uuid -> lab uuid
        adds 1 to the borrowed assets
        """
        count = Asset.objects.filter(
            category_type_id=asset.category_type_id,
            Lab_id=uuid,
            status="Borrowed",
        ).count()
        category = AssetCategory.objects.get(asset=asset)
        category.borrowed_assets = count
        print(count)
        print(category.borrowed_assets)
        category.save()

    @staticmethod
    def reduce_borrowed_assets(asset, uuid):
        """
        asset -> asset category instance
        uuid -> lab uuid
        reduces 1 to the borrowed assets
        """
        count = Asset.objects.filter(
            category_type_id=asset.category_type_id,
            Lab_id=uuid,
            status="Borrowed",
        ).count()
        category = AssetCategory.objects.get(asset=asset)
        category.borrowed_assets = count
        print(category.borrowed_assets)
        print(count)
        category.save()

    @staticmethod
    def getAssetByLabSupervisor(x):
        """
        get list of assets by lab supervisor
        x = lab supervisor
        """
        return AssetCategory.objects.filter(Lab__supervisor=x)


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
        related_name="asset",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    Lab = models.ForeignKey(
        Lab,
        verbose_name="lab / Lab",
        on_delete=models.CASCADE,
    )
    pic = models.ImageField(
        _(" asset image"),
        upload_to=asset_photo_upload,
        null=False,
    )
    status = models.CharField(
        _("asset status"),
        choices=asset_status,
        max_length=50,
    )
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
        get the assets of Lab x
        """
        return Asset.objects.filter(Lab=x)

    @staticmethod
    def getSingleAsset(x):
        """
        get a single  assets
        x = item primary key
        """
        return Asset.objects.get(pk=x)

    @staticmethod
    def getAssetsByCategory(x):
        """
        get list of objects by category type and Lab ID
        x-> category item id
        """
        return Asset.objects.filter(category_type_id=x,)

    @staticmethod
    def getAvailbleAssets(x):
        """
        get the available assets of Lab x
        """
        return Asset.objects.filter(Lab=x, status="Available")


class Borrowed_Asset(models.Model):
    """
    models for the assets dorrowed
    """

    asset = models.ForeignKey(
        Asset,
        verbose_name="borrowed item",
        on_delete=models.CASCADE,
        related_name="borrowed_asset",
    )
    lab = models.ForeignKey(
        Lab,
        verbose_name="lab",
        on_delete=models.CASCADE,
    )
    person = models.CharField(
        _("borrowers name(one)"), max_length=50, blank=False, null=False
    )
    student_id = models.CharField(
        _("student id"), max_length=50, blank=False, null=False
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
    received_by = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="borrowed_asset_receiver",
        verbose_name="received by",
        null=True,
        blank=True,
    )
    issued_out_by = models.ForeignKey(
        Account,
        related_name="borrowed_asset_issued_out",
        on_delete=models.CASCADE,
        verbose_name="issued out by",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Borrowd Asset")
        verbose_name_plural = _("Borrowd Assets")
        ordering = ["returned_on"]

    def __str__(self):
        return f"{self.asset}"

    @staticmethod
    def getBorrowedAssets(x):
        """
        get the assets of Lab x, that are borrowed
        """
        return Borrowed_Asset.objects.filter(lab_id=x)

    @staticmethod
    def getSingleBorrowedAssets(x):
        """
        get the single borrowed using the records pk
        """
        return Borrowed_Asset.objects.get(pk=x)

    @staticmethod
    def getAssetByPK(x):
        """
        returns the lates infomation about an asset by it primary key
        """
        return Borrowed_Asset.objects.filter(asset=x).last()
