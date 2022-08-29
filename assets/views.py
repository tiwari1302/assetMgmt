from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import asset, assetType, User
from .forms import UserRegisterForm, UserUpdateForm, createAssetForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

class SuperUserCheck(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

@user_passes_test(lambda u: u.is_superuser)
def adminAssetView(request):
    context = {
        'assets': asset.objects.all(),
        'users':User.objects.all(),
    }
    return render(request, 'assets/assetAdmin.html', context)

@user_passes_test(lambda u: u.is_superuser)
def createAssetView(request):
    assetTypeList = assetType.objects.all()  # use assetType.title
    assettype = request.POST.get('asset-type')
    assetname = request.POST.get('asset-name')
    locationn = request.POST.get('location')
    brandd = request.POST.get('brand')
    purchaseyear = request.POST.get('purchase-year')
    isActivve = request.POST.get('is-active','') == 'on'
    cuser=request.user
    context={
        "cuser":request.user,
        "asset_type_list":assetTypeList,
        "asset_type":assettype,
        "asset_name":assetname,
        "location":locationn,
        "brand":brandd,
        "purchase_year":purchaseyear,
        "isActive":isActivve,
        'iterator':range(2014,2050)
    }
    if request.method == 'POST':
        new_asset = asset()
        target_type = assetType.objects.get(title=assettype)
        new_asset.asset_type = target_type
        # new_asset.asset_type_title=request.POST.get('asset-type')
        new_asset.asset_name=assetname
        new_asset.location=locationn
        new_asset.brand=brandd
        new_asset.purchase_year=purchaseyear
        new_asset.isActive=True if isActivve else False
        new_asset.currentOwner=cuser
        new_asset.save()
        return redirect('createAssets')
    
    return render(request, 'assets/createAsset.html', context)

# @login_required
@user_passes_test(lambda u: u.is_active)
def assets(request):
    asset_o = asset.objects.filter(currentOwner=request.user)
    context = {
        'assets': asset_o.all(),
    }
    return render(request, 'assets/asset.html', context)

class assetUpdateView(SuperUserCheck, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = asset
    slug_url_kwarg = 'id'
    slug_field = 'id'
    fields = ['asset_name', 'asset_type', 'currentOwner']
    template_name = 'assets/updateAsset.html'
    success_url="../../assetAdmin"
    # context_object_name = 'assets'
    # slug_url_kwarg = "username"
    # slug_field = "username"
    # def form_valid(self, form):
    #     return super().form_valid(form)

# @login_required
def home(request):
    context = {
        
    }
    return render(request, 'assets/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'assets/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES , instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')        
    else:
        u_form = UserUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        # 'p_form': p_form,
    }
    return render(request, 'assets/profile.html', context)


