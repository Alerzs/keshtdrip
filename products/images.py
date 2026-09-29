from pathlib import Path

from django.conf import settings
from django.templatetags.static import static


def image_src(value):
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    prefix = settings.STATIC_URL
    if value.startswith(prefix):
        relative = value[len(prefix) :]
    elif value.startswith("/"):
        return value
    else:
        relative = value.lstrip("/")
    try:
        return static(relative)
    except ValueError:
        return prefix + relative


def sibling_image_urls(url):
    prefix = settings.STATIC_URL
    if not url or not url.startswith(prefix):
        return []
    rel = Path(url[len(prefix) :])
    folder = _static_dir(rel.parent)
    if folder is None:
        return []
    extras = []
    stem = rel.stem
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}:
            continue
        if path.stem == stem:
            continue
        suffix = path.stem[len(stem) :] if path.stem.startswith(stem) else ""
        if not suffix.lstrip("-_").isdigit():
            continue
        stored = f"{prefix}{(rel.parent / path.name).as_posix()}"
        extras.append(image_src(stored))
    return extras


def _static_dir(relative):
    roots = [Path(root) for root in settings.STATICFILES_DIRS]
    static_root = getattr(settings, "STATIC_ROOT", None)
    if static_root:
        roots.append(Path(static_root))
    for root in roots:
        folder = root / relative
        if folder.is_dir():
            return folder
    return None
