#!/usr/bin/env python3
"""
collect_frontend.py – Concatène automatiquement les fichiers clés du front-end
Exécuté depuis la racine du front-end (à côté de package.json)
Résultat : bundle_frontend.md
"""

from pathlib import Path
import sys

# Racine du projet
root = Path(__file__).resolve().parent

# Fichiers racine obligatoires
ROOT_REQUIRED = [
    "package.json",
    "pnpm-lock.yaml",
    "next.config.ts",
    "tsconfig.json",
    "tailwind.config.js",
    "postcss.config.js",
    "eslint.config.mjs",
    "jest.config.js",
    "playwright.config.ts",
    "app/layout.tsx",
    "app/page.tsx",
    "app/ClientProviders.tsx",
    "app/StyledComponentsRegistry.tsx",
    "components/layout-components/Header.tsx",
    "components/layout-components/MainLayout.tsx",
    "components/Button/Button.tsx",
    "instrumentation.ts",
    "env.mjs",
]
# Fichiers racine optionnels
ROOT_OPTIONAL = [
    ".env.local",
    ".env.example",
    "theme.ts",
]

# Génère la liste des fichiers à concaténer
def yield_target_files():
    # 1. Fichiers obligatoires
    for rel in ROOT_REQUIRED:
        yield root / rel, True
    # 2. Fichiers optionnels s'ils existent
    for rel in ROOT_OPTIONAL:
        path = root / rel
        if path.exists():
            yield path, False

# Fichier de sortie
output = root / "bundle_frontend.md"
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
