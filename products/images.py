from pathlib import Path

from django.conf import settings
from django.templatetags.static import static


def image_src(value):
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    relative = _static_relative(value)
    if not relative:
        return value if value.startswith("/") else ""
    try:
        return static(relative)
    except ValueError:
        return settings.STATIC_URL + relative


def image_fit(value, width):
    relative = _static_relative(value)
    if relative:
        path = Path(relative)
        variant = path.with_name(f"{path.stem}-w{int(width)}.webp").as_posix()
        if _static_file(variant) is not None:
            return image_src(variant)
    return image_src(value)


def _static_relative(value):
    value = (value or "").strip()
    if not value or value.startswith(("http://", "https://")):
        return ""
    prefix = settings.STATIC_URL
    if value.startswith(prefix):
        return value[len(prefix) :]
    if value.startswith("/"):
        return ""
    return value.lstrip("/")


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


def _static_roots():
    roots = [Path(root) for root in settings.STATICFILES_DIRS]
    static_root = getattr(settings, "STATIC_ROOT", None)
    if static_root:
        roots.append(Path(static_root))
    return roots


def _static_file(relative):
    relative = Path(relative)
    for root in _static_roots():
        file = root / relative
        if file.is_file():
            return file
    return None


def _static_dir(relative):
    for root in _static_roots():
        folder = root / relative
        if folder.is_dir():
            return folder
    return None
