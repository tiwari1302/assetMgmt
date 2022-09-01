import django_filters
from .models import asset, assetType, User

class ListingFilter(django_filters.FilterSet):

    class Meta:
        model = asset
        fields = {
            'currentOwner': ['exact'],
            # 'brand': ['exact'],
            'asset_type': ['exact'],
            # 'asActive' : ['exact'],   
        }

# class TypeFilter(django_filters.FilterSet):

#     class Meta:
#         model = assetType
#         fields=['title']