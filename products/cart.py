CART_SESSION_KEY = "cart"


def get_cart(session):
    return session.get(CART_SESSION_KEY, {})


def save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True


def line_key(product_id, variant_id=None):
    if variant_id:
        return f"{int(product_id)}v{int(variant_id)}"
    return str(int(product_id))


def parse_line_key(key):
    text = str(key)
    if "v" in text:
        product_id, variant_id = text.split("v", 1)
        return int(product_id), int(variant_id)
    return int(text), None


def add_item(session, product_id, quantity=1, variant_id=None):
    cart = get_cart(session)
    key = line_key(product_id, variant_id)
    cart[key] = cart.get(key, 0) + max(1, int(quantity))
    save_cart(session, cart)


def set_quantity(session, line_key, quantity):
    cart = get_cart(session)
    key = str(line_key)
    quantity = int(quantity)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    save_cart(session, cart)


def remove_item(session, line_key):
    cart = get_cart(session)
    cart.pop(str(line_key), None)
    save_cart(session, cart)


def clear_cart(session):
    save_cart(session, {})


def cart_count(session):
    return sum(get_cart(session).values())
