from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from cart.cart import Cart
from store.models import Product


def cart(request):
    cart = Cart(request)
    return render(request, 'store/cart/summary.html', {'cart': cart}) 

@require_POST
def cartAdd(request):
    cart = Cart(request) 

    productId = int(request.POST.get('product_id'))
    productQuantity = int(request.POST.get('product_quantity'))
    product = get_object_or_404(Product, id= productId)
    cart.add(product= product, quantity= productQuantity)

    cartQuantity = cart.__len__()
    
    return JsonResponse({'quantity': cartQuantity})

@require_POST
def cartDelete(request):
    cart = Cart(request)
    productId = int(request.POST.get('product_id'))
    cart.delete(product= productId)

    cartQuantity = cart.__len__()
    cartTotal = cart.get_total_price()

    return JsonResponse({'quantity': cartQuantity, 'subtotal': cartTotal})

@require_POST
def cartUpdate(request):
    cart = Cart(request)
    productId = int(request.POST.get('product_id'))
    productQuantity = int(request.POST.get('product_quantity'))
    cart.update(product= productId, quantity= productQuantity)

    cartQuantity = cart.__len__()
    cartTotal = cart.get_total_price()

    return JsonResponse({'quantity': cartQuantity, 'subtotal': cartTotal})    
