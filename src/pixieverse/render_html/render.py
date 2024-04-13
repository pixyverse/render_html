from typing import List


def createElement(elem: str, props: dict[str, str] = {}, children: List[str] = []):
    render_children = "".join(children)
    return f"<{elem}>{render_children}</{elem}>"
