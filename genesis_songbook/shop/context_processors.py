from shop.cart import Cart

def cart_context(request):
    """
    Make cart information available to all templates
    """
    try:
        cart = Cart(request)
        return {
            'cart_items_count': len(cart),
            'cart_total_price': cart.get_total_price(),
        }
    except Exception:
        # If there's any issue with the cart, return empty values
        return {
            'cart_items_count': 0,
            'cart_total_price': 0,
        }