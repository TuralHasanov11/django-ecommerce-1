from django.http.response import JsonResponse
from django.shortcuts import render

from cart.cart import Cart
from django.views.decorators.http import require_POST
from .models import Order, OrderItem

@require_POST
def add(request):
    cart = Cart(request)

    order_key = request.POST.get('order_key')
    userId = request.user.id
    cartTotal = cart.get_total_price()

    if Order.objects.filter(order_key=order_key).exists():
        pass
    else:
        order = Order.objects.create(user_id=userId, full_name='name', address1='add1',
                            address2='add2', total_paid=cartTotal, order_key=order_key)
        orderId = order.pk

        for item in cart:
            OrderItem.objects.create(order_id=orderId, product=item['product'], price=item['price'], quantity=item['quantity'])

    response = JsonResponse({'success': 'Return something'})
    return response


def paymentConfirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def userOrders(request):
    userId = request.user.id
    orders = Order.objects.prefetch_related("items").filter(user_id=userId).filter(billing_status=True)
    return orders