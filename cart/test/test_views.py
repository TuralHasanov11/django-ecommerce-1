from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from store.models import Category, Product


class TestCartView(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        Product.objects.create(category_id=1, title='django intermediate', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        Product.objects.create(category_id=1, title='django advanced', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        self.client.post(
            reverse('cart:cart_add'), {"product_id": 1, "product_quantity": 1}, xhr=True)
        self.client.post(
            reverse('cart:cart_add'), {"product_id": 2, "product_quantity": 2}, xhr=True)

    def test_cart_url(self):
        response = self.client.get(reverse('cart:cart_summary'))
        self.assertEqual(response.status_code, 200)

    def test_cart_add(self):
        response = self.client.post(
            reverse('cart:cart_add'), {"product_id": 3, "product_quantity": 1}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('cart:cart_add'), {"product_id": 2, "product_quantity": 1}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_cart_delete(self):
        response = self.client.post(
            reverse('cart:cart_delete'), {"product_id": 2}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})

    def test_cart_update(self):
        response = self.client.post(
            reverse('cart:cart_update'), {"product_id": 2, "product_quantity": 1}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})