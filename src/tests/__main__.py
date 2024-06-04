import unittest

import xmlrunner

# import your test modules
import tests.test_render

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(tests.test_render))


# initialize a runner, pass it your suite and run it
runner = xmlrunner.XMLTestRunner(verbosity=3, output="./junit", outsuffix="junit")
result = runner.run(suite)
