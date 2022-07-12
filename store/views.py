from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from django.views.decorators.http import require_GET

@require_GET
def products(request):
    products = Product.products.prefetch_related('product_image').all()
    return render(request, 'store/index.html', {'products': products})

@require_GET
def categoryProducts(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.products.prefetch_related('product_image').filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    )
    return render(request, 'store/category.html', {'category': category, 'products': products})

@require_GET
def productDetail(request, slug):
    product = Product.products.prefetch_related('product_image').filter(slug=slug)
    return render(request, 'store/detail.html', {'product': product})
    