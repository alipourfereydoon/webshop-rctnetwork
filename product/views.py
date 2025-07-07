from django.shortcuts import render
from django.views.generic import DetailView
from product.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name='product/product_detail.html'