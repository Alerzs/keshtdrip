from pathlib import Path

from django import template
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def amp_css(name):
    found = finders.find(name)
    if not found:
        return ""
    return mark_safe(Path(found).read_text(encoding="utf-8"))
