from .cart import cart_count


def shop(request):
    return {"cart_count": cart_count(request.session)}
