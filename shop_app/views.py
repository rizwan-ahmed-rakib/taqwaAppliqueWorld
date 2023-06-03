from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here for your models
from shop_app.models import Product, Category
# mixin
from django.contrib.auth.mixins import LoginRequiredMixin

"""classbase view"""


class Home(ListView):
    model = Product
    template_name = 'shop_app/home.html'


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'shop_app/product_detail.html'
