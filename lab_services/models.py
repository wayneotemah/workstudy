import uuid
import os
from django.db import models

def found_item_photo_upload(instance, filename):
    """
    Uploads a photo to the found item folder
    """
    return "media/found_item_photos/{0}/{1}".format(
        instance.id, os.path.splitext(filename))

class Found_Item(models.Model):
    """
    Model for items found in the lab
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    item_photo = models.ImageField(
        upload_to=found_item_photo_upload,
        blank=True,
        null=True)
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    date_found = models.DateField(auto_now_add=True)
    time_found = models.TimeField(auto_now_add=True,
                                  blank=True,
                                  null=True)
    lab = models.ForeignKey(
        "Labs.Lab",
         on_delete=models.CASCADE)

    def __str__(self):
       return self.item_name
