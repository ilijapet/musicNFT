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
    user_name = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField()
