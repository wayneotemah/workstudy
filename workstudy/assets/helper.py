from organizations.helper import UserDetailsHelper
from assets.models import Asset


class AssetsHelper(UserDetailsHelper):
    def __init__(self,user,uuid):
        super().__init__(user,uuid)

    def getAssets(self):
        return Asset.getAssets(self.companyUUID)
        
