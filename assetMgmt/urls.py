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
from assets.views import register, profile, assets, home, adminAssetView, createAssetView, assetUpdateView

urlpatterns = [
    path('home/', home, name='home'),
    path('assets/', assets, name='assets'),
    path('assetAdmin/', adminAssetView, name='assetsAdmin'),
    path('createAsset/', createAssetView, name='createAssets'),
    path('assetsupdate/<id>/', assetUpdateView.as_view(), name='asset-update'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='assets/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='assets/logout.html'), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('admin/', admin.site.urls),
]
