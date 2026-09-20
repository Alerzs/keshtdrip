import re

from django import template

register = template.Library()
_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_DESCRIPTION_SPLIT = re.compile(r"[\n\r]+|(?<=[.؟!])\s+")


@register.filter
def as_lines(value):
    text = str(value or "").strip()
    if not text:
        return []
    return [part.strip() for part in _DESCRIPTION_SPLIT.split(text) if part.strip()]


@register.filter
def fa_num(value):
    if value is None:
        return ""
    text = f"{value:,}".replace(",", "٬") if isinstance(value, int) else str(value)
    return text.translate(_DIGITS)
