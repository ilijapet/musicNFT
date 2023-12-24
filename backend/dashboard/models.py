from django.db import models


class NftMetadata(models.Model):
    name = models.CharField(verbose_name="band", max_length=100)
    description = models.CharField(max_length=2000)
    cover_file_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class OrderHistory(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    user_identifier = models.CharField(max_length=255, null=True, blank=True)
    # From NewUser
    user_name = models.CharField(max_length=255, null=True, blank=True)
    # From NftMetadata
    metadata_identifier = models.CharField(max_length=255, null=True, blank=True)
    profile_type = models.CharField(max_length=20)
    price = models.FloatField()
