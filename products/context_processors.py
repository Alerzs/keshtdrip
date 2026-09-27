from .cart import cart_count
from .seo import seo_for_request


def shop(request):
    return {
        "cart_count": cart_count(request.session),
        "seo": getattr(request, "seo", None) or seo_for_request(request),
    }
