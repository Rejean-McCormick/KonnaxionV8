#!/usr/bin/env python3
"""
AAconcatMainFilesBack.py – Concatène automatiquement les fichiers clés de chaque app Django
Exécuté depuis la racine du backend (à côté de package.json ou pyproject.toml)
Résultat : bundle_backend.md
"""

from pathlib import Path
import sys

# Racine du projet
root = Path(__file__).resolve().parent

# Fichiers racine obligatoires (hors apps/)
ROOT_REQUIRED = [
    "manage.py",
    "config/settings/base.py",
    "config/settings/local.py",
    "config/settings/production.py",
    "config/urls.py",
    "asgi.py",
    "wsgi.py",
    "pyproject.toml",
    "requirements/local.txt",
    "requirements/production.txt",
    "Procfile",
]
# Fichiers racine optionnels
ROOT_OPTIONAL = [
    "docker-compose.yml",
]

# Fichiers obligatoires dans chaque app
APP_REQUIRED = [
    "apps.py",
    "admin.py",
    "models.py",
    "serializers.py",
    "views.py",
    "urls.py",
    "migrations/0001_initial.py",
]
# Fichiers optionnels dans chaque app
APP_OPTIONAL = [
    "forms.py",
    "tasks.py",
    "permissions.py",
]

# Fonction de détection d'app
def is_django_app(d: Path) -> bool:
    return (d / "models.py").exists()

# Génère la liste des fichiers à concaténer
def yield_target_files():
    # 1. Fichiers root obligatoires
    for rel in ROOT_REQUIRED:
        yield root / rel, True
    # 2. Fichiers root optionnels
    for rel in ROOT_OPTIONAL:
        path = root / rel
        if path.exists():
            yield path, False
    # 3. Apps découvertes dynamiquement
    apps_dir = root / "apps"
    if not apps_dir.is_dir():
        sys.exit("❌ Dossier 'apps/' introuvable ; placez le script à la racine du projet !")
    for app_path in apps_dir.rglob("*"):
        if app_path.is_dir() and is_django_app(app_path):
            # requiered
            for f in APP_REQUIRED:
                yield app_path / f, True
            # optional
            for f in APP_OPTIONAL:
                path = app_path / f
                if path.exists():
                    yield path, False

# Exécution et écriture
output = root / "bundle_backend.md"
missing_required = []
written = 0

with output.open("w", encoding="utf-8") as out:
    for path, required in yield_target_files():
        if not path.exists():
            if required:
                missing_required.append(path.relative_to(root))
            continue
        rel = path.relative_to(root)
        lang = path.suffix.lstrip('.')
        out.write(f"\n\n---\n## {rel}\n\n```{lang}\n")
        out.write(path.read_text(encoding="utf-8", errors="replace"))
        out.write("\n```\n")
        written += 1

# Affichage des résultats
print(f"✅  {written} fichiers ajoutés à {output}")
if missing_required:
    print(f"⚠️  Fichiers requis introuvables ({len(missing_required)}) :")
    for m in missing_required:
        print(f"  - {m}")
