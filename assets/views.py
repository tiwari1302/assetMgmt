from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.models import User
from .models import asset, assetType

class AssetTypeListView(ListView):
    model = assetType
    template_name = ''
    context_object_name = 'types'
    paginate_by = 5