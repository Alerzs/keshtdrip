from django import template

from products.images import image_fit as resolve_image_fit
from products.images import image_src as resolve_image_src

register = template.Library()


@register.filter
def image_src(value):
    return resolve_image_src(value)


@register.filter
def image_fit(value, width):
    return resolve_image_fit(value, width)
