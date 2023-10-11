from typing import Type
from .abstract import Extension

EXTENSION_NAMES = {"gcal", "todotxt"}


def get_extension(name: str) -> Type[Extension]:
    if name == "gcal":
        from .gcal import gcal_ext

        return gcal_ext
    elif name == "todotxt":
        from .todotxt import todotxt_ext

        return todotxt_ext
    else:
        raise ValueError(f"Unknown extension: {name}")
