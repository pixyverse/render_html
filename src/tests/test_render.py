import contextlib
from io import StringIO
import sys
import unittest
from pixieverse.pixie.transpile import transpile_source


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


class TestRender(unittest.TestCase):
    def test_RenderMinimal(self):
        input = """
from src.pixieverse.render_html.render import createElement
comp=<p></p>
print(comp)
"""
        expected = """<p></p>
"""
        source = transpile_source(input)
        with stdoutIO() as output:
            try:
                exec(source, globals())
            except Exception as ex:
                self.fail(f"Unable to execute source {ex}")
        self.assertEqual(expected, output.getvalue())

    def test_RenderNested(self):
        input = """
from src.pixieverse.render_html.render import createElement
comp=<p><h1></h1></p>
print(comp)
"""
        expected = """<p><h1></h1></p>
"""
        source = transpile_source(input)
        with stdoutIO() as output:
            try:
                exec(source, globals())
            except Exception as ex:
                self.fail(f"Unable to execute source {ex}")
        self.assertEqual(expected, output.getvalue())

    def test_RenderMultipleNested(self):
        input = """
from src.pixieverse.render_html.render import createElement
comp=<p><h1></h1><h2></h2></p>
print(comp)
"""
        expected = """<p><h1></h1><h2></h2></p>
"""
        source = transpile_source(input)
        with stdoutIO() as output:
            try:
                exec(source, globals())
            except Exception as ex:
                self.fail(f"Unable to execute source {ex}")
        self.assertEqual(expected, output.getvalue())

    def test_RenderMultipleNested(self):
        input = """
from src.pixieverse.render_html.render import createElement
comp=<p><h1></h1><h2></h2></p>
print(comp)
"""
        expected = """<p><h1></h1><h2></h2></p>
"""
        source = transpile_source(input)
        with stdoutIO() as output:
            try:
                exec(source, globals())
            except Exception as ex:
                self.fail(f"Unable to execute source {ex}")
        self.assertEqual(expected, output.getvalue())

    def test_RenderComponent(self):
        input = """
from src.pixieverse.render_html.render import createElement

def header_comp(tagName, props, children):
    return (<p><h1></h1><h2></h2></p>)

comp=<header_comp></header_comp>
print(comp)
"""
        expected = """<p><h1></h1><h2></h2></p>
"""
        source = transpile_source(input)
        with stdoutIO() as output:
            try:
                exec(source, globals())
            except Exception as ex:
                self.fail(f"Unable to execute source: {ex}")
        self.assertEqual(expected, output.getvalue())

    def test_RenderComponentChildren(self):
        input = """
from src.pixieverse.render_html.render import createElement

def menu_comp(tagName, props, children):
    return <ul><li></li></ul>

def header_comp(tagName, props, children):
    return (<h1><menu_comp></menu_comp></h1>)

comp=<header_comp></header_comp>
print(comp)
"""
        expected = """<h1><ul><li></li></ul></h1>
"""
        source = transpile_source(input)
        with stdoutIO() as output:
            try:
                exec(source, globals())
            except Exception as ex:
                self.fail(f"Unable to execute source: {ex}")
        self.assertEqual(expected, output.getvalue())
