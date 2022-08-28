from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm
from .models import asset, assetType

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class createAssetForm(forms.Form):
    model = asset
    asset_type = forms.ChoiceField(choices=assetType.objects.all())
    asset_name = forms.CharField(max_length = 30)
    location = forms.CharField(max_length = 30)
    brand = forms.CharField(max_length = 30)
    purchase_year = forms.DateField()
    isActive = forms.BooleanField()
        
        # fields = ['asset_type', 'asset_name', 'location', 'brand', 'purchase_year', 'isActive']
