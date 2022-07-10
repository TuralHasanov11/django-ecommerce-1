from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.products, name='products'),
    path('<slug:slug>', views.productDetail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.categoryProducts, name='category_products'),
]