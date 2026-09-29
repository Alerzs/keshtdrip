from django import template

from products.images import image_src as resolve_image_src

register = template.Library()


@register.filter
def image_src(value):
    return resolve_image_src(value)
