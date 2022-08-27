from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class assetType(models.Model):
    title = models.CharField(max_length=150)

    @property
    def get_type(self):
        return asset.objects.filter(asset_type=self.id)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = 'Asset Types'

class asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_type = models.ForeignKey('assetType', on_delete=models.CASCADE)
    asset_name = models.CharField(max_length=30, unique=True)
    location = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    purchase_year = models.PositiveIntegerField(blank=True, null=True)
    isActive = models.BooleanField(default=True)
    currentOwner = models.ForeignKey(User, default='', on_delete=models.CASCADE)