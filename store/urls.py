from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.products, name='products'),
    path('item/<slug:slug>/', views.productDetail, name='product_detail'),
    path('search/<slug:category_slug>/', views.categoryProducts, name='category_products'),
]