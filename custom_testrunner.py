# custom_testrunner.py
import xmlrunner
from django.test.runner import DiscoverRunner

class CustomTestRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        return xmlrunner.XMLTestRunner(
            output='test-reports',
            verbosity=self.verbosity,
            failfast=self.failfast,
            buffer=False
        ).run(suite)
