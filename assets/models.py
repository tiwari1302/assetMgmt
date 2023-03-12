from django.db import models

import uuid
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
# Create your models here.

class assetType(models.Model):
    title = models.CharField(max_length=150)

    # @property
    # def get_type(self):
    #     return asset.objects.filter(asset_type=self.id)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = 'Asset Types'

def get_superuser():
    su_user = User.objects.filter(is_superuser=True).first()
    if su_user:
        return su_user.pk
    raise DoesNotExist('Please add Super User')


class asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    asset_type = models.ForeignKey('assetType', on_delete=models.CASCADE, null=True)
    asset_name = models.CharField(max_length=30, null=True) #unique=True
    location = models.CharField(max_length=30, null=True)
    brand = models.CharField(max_length=30, null=True)
    purchase_year = models.PositiveIntegerField(blank=True, null=True)
    isActive = models.BooleanField(default=True, null=True)
    currentOwner = models.ForeignKey(User, default=get_superuser, null=False, on_delete=models.SET_DEFAULT) #User.objects.get(is_superuser=True).id

class Transaction(models.Model):
    transferredAsset = models.ForeignKey(asset, null=True, blank=True, on_delete=models.CASCADE)
    oldOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="oldOwnerName")
    newOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="newOwnerName")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)