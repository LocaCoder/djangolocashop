from .cart import Cart


def show_cart(request):
    return {'cart': Cart(request)}
