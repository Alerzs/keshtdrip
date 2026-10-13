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


@register.simple_tag
def image_alt(name, spec="", group="", index="", code=""):
    parts = [" ".join(str(name or "").split()) or "تصویر محصول"]
    spec = " ".join(str(spec or "").split())
    group = " ".join(str(group or "").split())
    code = " ".join(str(code or "").split())
    if spec:
        parts.append(spec)
    if group:
        parts.append(group)
    if index not in ("", None):
        parts.append(str(index))
    if code:
        parts.append(code)
    return "، ".join(parts)
