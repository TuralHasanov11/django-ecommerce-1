from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.cartView, name='cart'),
    path('order-placed/', views.orderPlaced, name='order_placed'),
    path('error/', views.Error.as_view(), name='error'),
    path('webhook/', views.stripeWebhook),
]