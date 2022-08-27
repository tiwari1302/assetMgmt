from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import assetType, asset, User, User_manager

# admin.site.register(asset)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "gender")
    list_filter = ("is_superuser",)

@admin.register(assetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ("title", )

@admin.register(asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "asset_name", "asset_type", "brand", "isActive", "currentOwner")
    list_filter = ("asset_type", "currentOwner")