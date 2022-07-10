from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/', views.cartAdd, name='cart_add'),
    path('update/', views.cartUpdate, name='cart_update'),
    path('delete/', views.cartDelete, name='cart_delete'),
]