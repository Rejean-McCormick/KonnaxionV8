#!/usr/bin/env python
import os
import sys

# Determine the project root (where this script is located)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# Add the project root to sys.path (if needed)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Also add the apps folder to sys.path so that "common" and other apps can be imported directly.
apps_dir = os.path.join(project_root, "apps")
if apps_dir not in sys.path:
    sys.path.insert(0, apps_dir)

print("Project root:", project_root)
print("Apps directory added to sys.path:", apps_dir)
print("Current sys.path:")
for p in sys.path:
    print("  ", p)

# Test if the 'common' module can be imported.
try:
    import common
    print("Successfully imported 'common'")
except Exception as e:
    print("Error importing 'common':", e)

# Now import Django and set up the environment.
import django
from django.apps import apps
from django.core.management import call_command

# Set BASE_DIR to point to your local apps folder.
BASE_DIR = apps_dir  # now BASE_DIR == C:\MonCode\KonnaxionV4\apps
print("Local apps directory (BASE_DIR):", BASE_DIR)

def is_local_app(app_config):
    """Return True if the app's code is under the local apps folder (BASE_DIR)."""
    return app_config.path.startswith(BASE_DIR)

def create_initial_migration_if_needed(app_config):
    """
    For the given app, if no migration files (other than __init__.py) exist in its
    migrations folder, create an empty initial migration.
    """
    migrations_dir = os.path.join(app_config.path, "migrations")
    if not os.path.isdir(migrations_dir):
        print(f"[{app_config.label}] Migrations folder not found at {migrations_dir}. Skipping.")
        return

    try:
        files = os.listdir(migrations_dir)
    except Exception as e:
        print(f"[{app_config.label}] Error listing files in {migrations_dir}: {e}")
        return

    # Consider only Python files that are not the __init__.py file.
    migration_files = [f for f in files if f.endswith(".py") and f != "__init__.py"]
    if not migration_files:
        print(f"[{app_config.label}] No migration files found. Creating an empty initial migration.")
        try:
            call_command("makemigrations", app_config.label, "--empty", "--name", "initial")
        except Exception as e:
            print(f"[{app_config.label}] Error creating migration: {e}")
    else:
        print(f"[{app_config.label}] Migration files exist: {migration_files}")

def main():
    # Set the Django settings module.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
    django.setup()

    print("Scanning local apps under:", BASE_DIR)
    for app_config in apps.get_app_configs():
        if is_local_app(app_config):
            print(f"Processing app: {app_config.label} (path: {app_config.path})")
            create_initial_migration_if_needed(app_config)
        else:
            print(f"Skipping external app: {app_config.label} (path: {app_config.path})")

if __name__ == "__main__":
    main()
