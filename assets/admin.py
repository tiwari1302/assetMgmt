from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
<<<<<<< HEAD
from .models import assetType, asset, User, Transaction #User_manager,

# admin.site.register(asset)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ("id", "username", "gender")
#     list_filter = ("is_superuser",)
=======
from .models import assetType, asset, User, User_manager, Transaction

# admin.site.register(asset)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "gender")
    list_filter = ("is_superuser",)
>>>>>>> 426b3357b6a219d0766822395d8bcbaeacea9c73

@admin.register(assetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)

@admin.register(asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "asset_name", "asset_type", "brand", "isActive", "currentOwner")
<<<<<<< HEAD
    list_filter = ("asset_type", "currentOwner", "brand")
=======
    list_filter = ("asset_type", "currentOwner")
>>>>>>> 426b3357b6a219d0766822395d8bcbaeacea9c73

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'transferredAsset', 'oldOwner', 'newOwner', 'timestamp')