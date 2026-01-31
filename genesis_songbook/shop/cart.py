from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, size=None):
        """
        Add a product to the cart or update its quantity.
        """
        # Create a unique key for product + size combination
        if size and product.is_clothing:
            product_key = f"{product.id}_{size}"
        else:
            product_key = str(product.id)
            
        if product_key not in self.cart:
            self.cart[product_key] = {
                'quantity': 0,
                'price': str(product.price),
                'product_id': product.id,
                'size': size if product.is_clothing else None
            }
        if override_quantity:
            self.cart[product_key]['quantity'] = quantity
        else:
            self.cart[product_key]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product, size=None):
        """
        Remove a product from the cart.
        """
        if size and product.is_clothing:
            product_key = f"{product.id}_{size}"
        else:
            product_key = str(product.id)
            
        if product_key in self.cart:
            del self.cart[product_key]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        # Get all unique product IDs from cart keys
        product_ids = set()
        for key in self.cart.keys():
            if '_' in key:  # Product with size
                product_id = key.split('_')[0]
            else:  # Product without size
                product_id = key
            product_ids.add(int(product_id))
        
        # Get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        products_dict = {product.id: product for product in products}
        
        cart = self.cart.copy()
        for key, item in cart.items():
            if '_' in key:
                product_id = int(key.split('_')[0])
            else:
                product_id = int(key)
            
            if product_id in products_dict:
                item['product'] = products_dict[product_id]
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                item['cart_key'] = key  # Store the cart key for removal
                yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()