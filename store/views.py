from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def products(request):
    products = Product.products.all()
    return render(request, 'store/index.html', {'products': products})


def categoryProducts(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.filter(category=category)
    return render(request, 'store/category.html', {'category': category, 'products': products})


def productDetail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/detail.html', {'product': product})
    