#!/usr/bin/env python
# ruff: noqa
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # Set the default settings module to the local settings.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # Add the current directory (project root) and the 'apps' folder to sys.path.
    current_path = Path(__file__).parent.resolve()
    sys.path.insert(0, str(current_path))
    apps_path = current_path / "apps"
    sys.path.insert(0, str(apps_path))

    execute_from_command_line(sys.argv)
