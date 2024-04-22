from typing import List


def createElement(elem: str, props: dict[str, str] = {}, children: List[str] = []):
    if elem[0:1].islower():
        render_children = "".join(children)
        return f"<{elem}>{render_children}</{elem}>"
    else:
        raise NotImplementedError
