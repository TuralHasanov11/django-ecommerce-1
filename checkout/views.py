import json

from account.models import Address
from cart.cart import Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from orders.models import Order, OrderItem
from django.views.decorators.http import require_POST
from .models import DeliveryOptions


@login_required
def deliveryChoices(request):
    deliveryOptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryOptions": deliveryOptions})

@require_POST
@login_required
def cartUpdateDelivery(request):
    cart = Cart(request)
    deliveryOption = int(request.POST.get("deliveryoption"))
    deliveryType = DeliveryOptions.objects.get(id=deliveryOption)
    updatedTotalPrice = cart.cart_update_delivery(deliveryType.delivery_price)

    session = request.session
    if "purchase" not in request.session:
        session["purchase"] = {
            "delivery_id": deliveryType.id,
        }
    else:
        session["purchase"]["delivery_id"] = deliveryType.id
        session.modified = True

    response = JsonResponse({"total": updatedTotalPrice, "delivery_price": deliveryType.delivery_price})
    return response


@login_required
def deliveryAddress(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def paymentSelection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    return render(request, "checkout/payment_selection.html", {})


####
# PayPay
####
from paypalcheckoutsdk.orders import OrdersGetRequest

from .paypal import PayPalClient


@login_required
def paymentComplete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value

    cart = Cart(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in cart:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False)


@login_required
def paymentSuccessful(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "checkout/payment_successful.html", {})