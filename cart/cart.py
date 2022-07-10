from decimal import Decimal

from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity):
        productId = str(product.id)

        if productId in self.cart:
            self.cart[productId]['quantity'] = quantity
        else:
            self.cart[productId] = {'price': str(product.price), 'quantity': quantity}

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

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def delete(self, product):
        productId = str(product)

        if productId in self.cart:
            del self.cart[productId]
            print(productId)
            self.save()

    def save(self):
        self.session.modified = True

