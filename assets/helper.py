from organizations.helper import UserDetailsHelper
from assets.models import Asset, Borrowd_Asset, AssetCategory


class AssetsHelper(UserDetailsHelper):
    def __init__(self, user, uuid):
        super().__init__(user, uuid)

    def getAssets(self):
        return Asset.getAssets(self.companyUUID)

    def getAssetCategoryList(self):
        return AssetCategory.getCategoryListByOrganization(self.companyUUID)

    def getBorrowesAssets(self):
        return Borrowd_Asset.getBorrowedAssets(self.companyUUID)

    def getAvailbleAssets(self):
        return Asset.getAvailbleAssets(self.companyUUID)
