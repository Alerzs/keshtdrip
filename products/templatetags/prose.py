from django import template

from products.prose import pack_blocks, tighten as tighten_text

register = template.Library()


@register.filter
def tighten(value):
    return tighten_text(value)


@register.inclusion_tag("shop/_prose.html")
def prose(text, class_name="leading-8 text-slate-600"):
    return {"blocks": pack_blocks(text or ""), "class_name": class_name}
