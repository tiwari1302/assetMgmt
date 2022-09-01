from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import asset, assetType, User, Transaction
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .filters import ListingFilter

# Create your views here.

def testView(request):
    assets = asset.objects.all()
    
    brandList = []
    typeList = []
    locationList = []
    purchaseYearList = []
    for a in assets:
        brandList.append(a.brand)
        typeList.append(a.asset_type)
        locationList.append(a.location)
        purchaseYearList.append(a.purchase_year)
    
    context = {
        'assets':assets,
        'brandList':set(brandList),
        'typeList':set(typeList),
        'purchaseYearList':set(purchaseYearList),
        
    }
    return render(request, 'assets/test.html', context)

class SuperUserCheck(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

@user_passes_test(lambda u: u.is_superuser)
def adminAssetView(request):
    assets = asset.objects.all()
    assetTypes = assetType.objects.all()
    users = User.objects.all()
    asset_filter = ListingFilter(request.GET, queryset=assets)
    
    # print(type(assets))
    # print(type(asset_filter.qs))
    context = {
        'assets': assets,
        'assetTypes': assetTypes,
        'users':users,
        'asset_filter':asset_filter,
    }

    action = request.POST.get('action')
    if action == "Delete selected asset(s)":
        # print("if statement working")
        assetList = request.POST.getlist('assetList[]') # returning id of assetType in list
        for t in assetList:
            obj = asset.objects.filter(id=t)
            obj.delete()
        
        # pass
        return redirect('assetsAdmin')
    return render(request, 'assets/assetAdmin.html', context)

@user_passes_test(lambda u: u.is_superuser)
def transactionsView(request):
    context = {}
 
    # add the dictionary during initialization
    context["transactions"] = Transaction.objects.all()
         
    return render(request, "assets/transactions.html", context)

class AssetTypeCreateView(CreateView, LoginRequiredMixin, SuperUserCheck):
    model = assetType
    fields = ['title']
    success_url="../../assetTypes"
    def form_valid(self, form):
        return super().form_valid(form)

def AssetTypeUpdateView(request, pk):
    obj = get_object_or_404(assetType, id=pk)
    oldTitle = obj.title

    if request.method=='POST':
        obj.title=request.POST.get('title')
        obj.save()
        return redirect('asset-type-list')

    context = {
        'obj' : obj,
    }

    return render(request, "assets/assetType_update.html", context)

@user_passes_test(lambda u: u.is_superuser)
def AssetTypeListView(request):
    types = assetType.objects.all()
    context = {
        'types' : types,
    }

    action = request.POST.get('action')
    if action == "Delete selected type(s)":
        # print("if statement working")
        assetTypeList = request.POST.getlist('typeList[]') # returning id of assetType in list
        for t in assetTypeList:
            obj = assetType.objects.filter(id=t)
            obj.delete()
        
        # pass
        return redirect('asset-type-list')

    return render(request, "assets/asset_types.html", context)

@user_passes_test(lambda u: u.is_superuser)
def createAssetView(request):
    assetTypeList = assetType.objects.all()  # use assetType.title
    assettype = request.POST.get('asset-type')
    assetname = request.POST.get('asset-name')
    locationn = request.POST.get('location')
    brandd = request.POST.get('brand')
    purchaseyear = request.POST.get('purchase-year')
    isActivve = request.POST.get('is-active') == 'Yes'
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
        'iterator':range(2014,2030)
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
        return redirect('assetsAdmin')
    
    return render(request, 'assets/createAsset.html', context)

# @login_required
@user_passes_test(lambda u: u.is_active)
def assets(request):
    asset_o = asset.objects.filter(currentOwner=request.user)
    context = {
        'assets': asset_o.all(),
    }
    return render(request, 'assets/asset.html', context)

@user_passes_test(lambda u: u.is_superuser)
def assetUpdateView(request, id):

    obj = get_object_or_404(asset, id=id)
    users = User.objects.all()
    assetTypeList = assetType.objects.all()
    oldOwner = obj.currentOwner
    oldType = obj.asset_type
    
    if request.method=='POST':
        
        newType = assetType.objects.get(title=request.POST.get('asset-type'))
        obj.asset_type = newType

        obj.asset_name = request.POST.get('asset-name')
        obj.location = request.POST.get('location')
        obj.brand = request.POST.get('brand')
        obj.purchase_year = request.POST.get('purchase_year')
        obj.isActive = request.POST.get('is-active')
        
        newOwner = User.objects.get(username=request.POST.get('current_owner'))
        obj.currentOwner = newOwner
        
        obj.save()
        if oldOwner != newOwner:
            new_transaction = Transaction(transferredAsset=obj, oldOwner=oldOwner, newOwner=newOwner)
            new_transaction.save()
        
        return redirect('assetsAdmin')
    context = {
        # "form" : form,
        "users": users,
        "obj" : obj,
        "asset_type_list":assetTypeList,
        'iterator':range(2014,2030),
    }
    return render(request, "assets/updateAsset.html", context)


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


