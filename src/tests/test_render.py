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
