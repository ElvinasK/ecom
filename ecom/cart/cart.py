from django.apps import apps
Product = apps.get_model('store', 'Product',)


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new , no session key ,create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make sure cart is available on all pages of site
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True


    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # use ids to lookup products in data base
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        # Get cart
        ourcart = self.cart

        # update dictionary / cart
        ourcart[product_id] = product_qty

        # update session
        self.session.modified = True

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * int(value)
                    else:
                        total += product.price * int(value)
        return total