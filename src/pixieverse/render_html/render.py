from typing import List

safeKeyNames = {"class_name": "class"}


def map_prop_name(name: str):
    if name in safeKeyNames.keys():
        return safeKeyNames[name]
    return name


def createElement(elem: str, props: dict[str, str] = {}, children: List[str] = []):
    render_children = "".join(children)
    return f"""<{elem}{''.join(f' {map_prop_name(key)}={value}' for key, value in props.items())}>{render_children}</{elem}>"""
