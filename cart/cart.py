from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity):
        productId = str(product.id)

        if productId in self.cart:
            self.cart[productId]['quantity'] = quantity
        else:
            self.cart[productId] = {'price': str(product.regular_price), 'quantity': quantity}

        self.save()

    def __iter__(self):
        productIds = self.cart.keys()
        products = Product.products.filter(id__in=productIds)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def update(self, product, quantity):
        productId = str(product)
        if productId in self.cart:
            self.cart[productId]['quantity'] = quantity
        self.save()

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        subtotal = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + Decimal(shipping)
        return total

    def delete(self, product):
        productId = str(product)

        if productId in self.cart:
            del self.cart[productId]
            print(productId)
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save() 

    def save(self):
        self.session.modified = True

