import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
import os
from django.conf import settings

from cart.cart import Cart
from orders.views import paymentConfirmation

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = 'whsec_28a2ee85649a3971e3a4e05c33c73e901487f9bcda58fe80323d86ecd7e00a68'

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
    data = request.body
    event = None

    try:
        event = stripe.Webhook.construct_event(
            data, request.headers.get('stripe-signature'), endpoint_secret
        )
    except ValueError as e:
        return JsonResponse(status_code=400, content=e)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse(status_code=400, content=e)

    if event.type == 'payment_intent.succeeded':
        paymentConfirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)