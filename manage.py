#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import xmlrunner


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'espoltel.settings')
    
    # Agregar la configuración de xmlrunner
    test_runner = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
    test_output_dir = 'test-reports'
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Insertar argumentos de línea de comandos para xmlrunner si no están presentes
    if 'test' in sys.argv and '--testrunner' not in sys.argv:
        sys.argv.extend(['--testrunner', test_runner])
    if 'test' in sys.argv and '--output' not in sys.argv:
        sys.argv.extend(['--output', test_output_dir])

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
