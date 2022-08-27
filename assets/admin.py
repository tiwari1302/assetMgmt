from django.contrib import admin

# Register your models here.
from .models import assetType, asset

# admin.site.register(assetType)
# admin.site.register(asset)

@admin.register(assetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ("title", )

@admin.register(asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("id", "asset_name", "asset_type", "brand", "isActive", "currentOwner")
    list_filter = ("asset_type", "currentOwner")