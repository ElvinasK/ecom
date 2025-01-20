from .cart import Cart
# Create context processor so our carrt can work on all pages
def cart(request):
    # Return default data from our cart
    return {'cart': Cart(request)}