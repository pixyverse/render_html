import keyword
from typing import Iterable, List

SPACER = " "


def map_prop_name(name: str):
    if name:
        lower_name = name.lower()
        prefix, suffix = (lower_name[:-1], lower_name[-1:])
        if suffix == "_" and prefix in [kw.lower() for kw in keyword.kwlist]:
            return prefix
    return name


def id(x):
    return x


def flat_map(f, xs: Iterable):
    ys: List = []
    for x in xs:
        ys.extend(f(x))
    return ys


def underscoreToHyphen(input: str) -> str:
    return input.replace("_", "-")


def render_attribute(key, value) -> str:
    if value in ["", False, None]:
        return ""
    return f"{SPACER}{underscoreToHyphen(map_prop_name(key))}={value}"


def create_element(
    elem: str,
    props: dict[str, str] = {},
    children: Iterable[str] | Iterable[Iterable[str]] = [],
):
    render_children = "".join(flat_map(id, children))
    return f"<{elem}\
{''.join(f'{render_attribute(key, value)}' for key, value in props.items())}>\
{render_children}</{elem}>"
