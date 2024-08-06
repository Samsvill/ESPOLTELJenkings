# testrunner.py
import xmlrunner
from django.test.runner import DiscoverRunner

class XMLTestRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        return xmlrunner.XMLTestRunner(
            output='test-reports',
            verbosity=self.verbosity,
            failfast=self.failfast,
            buffer=self.buffer
        ).run(suite)
