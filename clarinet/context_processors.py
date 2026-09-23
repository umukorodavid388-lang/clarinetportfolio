"""Artist details and press-kit link available in every template."""
from django.templatetags.static import static

from . import data


def site(request):
    return {
        "artist": data.ARTIST,
        "epk_url": static("files/press-kit.pdf"),
    }
