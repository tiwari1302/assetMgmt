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

@user_passes_test(lambda u: u.is_superuser)
def adminAssetView(request):
    context = {
        'assets': asset.objects.all(),
    }
    return render(request, 'assets/assetAdmin.html', context)

@user_passes_test(lambda u: u.is_superuser)
def createAssetView(request):
    # form = createAssetForm(request.POST)
    # if form.is_valid():
    #     print("form valid")
    # context = {

    # }
    # context['form'] = createAssetForm
    assetTypeList = assetType.objects.all()  # use assetType.title
    assettype = request.POST.get('asset-type')
    assetname = request.POST.get('asset-name')
    locationn = request.POST.get('location')
    brandd = request.POST.get('brand')
    purchaseyear = request.POST.get('purchase-year')
    isActivve = request.POST.get('is-active')
    context={
        "cuser":request.user,
        "asset_type_list":assetTypeList,
        "asset_type":assettype,
        "asset_name":assetname,
        "location":locationn,
        "brand":brandd,
        "purchase_year":purchaseyear,
        "is_active":isActivve,
    }
    if request.method == 'POST':
        new_asset = asset()
        new_asset.asset_type_title=assettype
        new_asset.asset_name=assetname
        new_asset.location=locationn
        new_asset.brand=brandd
        new_asset.purchase_year=purchaseyear
        new_asset.isActive=isActivve
        new_asset.save()
    return render(request, 'assets/createAsset.html', context)

# @login_required
@user_passes_test(lambda u: u.is_active)
def assets(request):
    # user = request.user
    # print(user)
    asset_o = asset.objects.filter(currentOwner=request.user)
    context = {
        'assets': asset_o.all(),
    }
    return render(request, 'assets/asset.html', context)

# @login_required
def home(request):
    # user = request.user
    # print(user)
    # asset_o = asset.objects.filter(currentOwner=request.user)
    context = {
        # 'assets': asset_o.all(),
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


