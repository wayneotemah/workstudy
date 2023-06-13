from Labs.helper import UserDetailsHelper
from assets.models import Asset, Borrowed_Asset, AssetCategory


class AssetsHelper(UserDetailsHelper):
    def __init__(self, user, uuid):
        super().__init__(user, uuid)

    def getAssets(self):
        return Asset.getAssets(self.companyUUID)

    def getAssetDetails(self, x):
        """
        return the one assets details
        x -> item primary key
        """
        return Asset.getSingleAsset(x)

    def getAssetCategoryList(self):
        return AssetCategory.getCategoryListByLab(self.companyUUID)

    def getBorrowesAssets(self):
        return Borrowed_Asset.getBorrowedAssets(self.companyUUID)

    def getAvailbleAssets(self):
        return Asset.getAvailbleAssets(self.companyUUID)
