import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
import os
from django.conf import settings

from cart.cart import Cart
from orders.views import paymentConfirmation

stripe.api_key = settings.STRIPE_SECRET_KEY

def orderPlaced(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/orderplaced.html')


class Error(TemplateView):
    template_name = 'payment/error.html'

@login_required
def cartView(request):

    cart = Cart(request)
    total = str(cart.get_total_price())
    total = int(total.replace('.', ''))

    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/index.html', {'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY'), 'client_secret': intent.client_secret})


@csrf_exempt
def stripeWebhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        paymentConfirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)