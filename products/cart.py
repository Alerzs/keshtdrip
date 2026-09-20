CART_SESSION_KEY = "cart"


def get_cart(session):
    return session.get(CART_SESSION_KEY, {})


def save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True


def add_item(session, product_id, quantity=1):
    cart = get_cart(session)
    key = str(product_id)
    cart[key] = cart.get(key, 0) + max(1, int(quantity))
    save_cart(session, cart)


def set_quantity(session, product_id, quantity):
    cart = get_cart(session)
    key = str(product_id)
    quantity = int(quantity)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    save_cart(session, cart)


def remove_item(session, product_id):
    cart = get_cart(session)
    cart.pop(str(product_id), None)
    save_cart(session, cart)


def clear_cart(session):
    save_cart(session, {})


def cart_count(session):
    return sum(get_cart(session).values())
