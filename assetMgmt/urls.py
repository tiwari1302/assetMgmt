"""assetMgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from assets.views import register, profile, assets, \
                            home, adminAssetView, AssetTypeCreateView,\
                            createAssetView, assetUpdateView, transactionsView, AssetTypeListView,\
                            AssetTypeUpdateView, testView

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('assets/', assets, name='assets'),
    path('assetsAdmin/', adminAssetView, name='assetsAdmin'),
    path('transactions/', transactionsView, name='transactions'),
    path('assetTypes/', AssetTypeListView, name='asset-type-list'),
    path('newAssetType/', AssetTypeCreateView.as_view(), name='asset-type-create'),
    path('updateAssetType/<pk>/', AssetTypeUpdateView, name='asset-type-update'),
    path('createAsset/', createAssetView, name='createAssets'),
    path('assetUpdate/<id>/', assetUpdateView, name='asset-update'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='assets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='assets/logout.html'), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('admin/', admin.site.urls),
    path('test/', testView, name='test'),
]
