import os
import django
from django.core.management import call_command
from django.test.runner import DiscoverRunner

os.environ["DJANGO_SETTINGS_MODULE"] = "espoltel.settings"

def before_all(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.old_db_config = context.test_runner.setup_databases()
    context.test_runner.setup_test_environment()
    context.test_case = DiscoverRunner()
    context.test_case.setup_test_environment()

def before_scenario(context, _):
    # Eliminar todos los datos de la base de datos antes de cada prueba
    call_command('flush', '--noinput')
    context.test_case.setUp()

def after_scenario(context, _):
    context.test_case.tearDown()

def after_all(context):
    context.test_case.tearDownClass()
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()
