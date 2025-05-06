#!/usr/bin/env python3
"""
Script pour Next.js App Router :  
Parcourt récursivement les fichiers .js, .jsx, .ts, .tsx  
Détecte ceux qui utilisent des hooks React ou next/navigation et qui doivent être des Client Components  
Ajoute 'use client' en tête de fichier s’il n’y est pas déjà
"""

import re
from pathlib import Path

# Extensions à scanner
EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx'}

# Dossiers à inclure
INCLUDE_DIRS = ['app', 'components', 'context', 'hooks']

# Patterns indiquant qu’un fichier doit être un Client Component
CLIENT_PATTERNS = [
    re.compile(r'\buseState\b'),
    re.compile(r'\buseEffect\b'),
    re.compile(r'\buseContext\b'),
    re.compile(r'\buseLayoutEffect\b'),
    re.compile(r'\buseRef\b'),
    re.compile(r'\buseMemo\b'),
    re.compile(r'\buseCallback\b'),
    re.compile(r'import\s+{[^}]*useRouter[^}]*}\s+from\s+[\'"]next\/router[\'"]'),
    re.compile(r'import\s+{[^}]*useRouter[^}]*}\s+from\s+[\'"]next\/navigation[\'"]'),
    re.compile(r'useServerInsertedHTML'),
]

def needs_use_client(text: str) -> bool:
    """Retourne True si le contenu text correspond à un Client Component."""
    return any(p.search(text) for p in CLIENT_PATTERNS)

def has_use_client(text: str) -> bool:
    """Vérifie si 'use client' est déjà présent en début de fichier."""
    # On autorise quelques commentaires ou lignes vides avant
    lines = text.splitlines()
    for line in lines[:5]:
        if re.match(r"^\s*['\"]use client['\"]\s*;?\s*$", line):
            return True
    return False

def process_file(path: Path):
    text = path.read_text(encoding='utf-8')
    if needs_use_client(text) and not has_use_client(text):
        print(f"→ Ajout de 'use client' dans {path}")
        # Insérer avant la première ligne de code significative
        lines = text.splitlines(keepends=True)
        # Trouver l’index après éventuelles directives shebang ou commentaires “use strict”
        insert_at = 0
        for i, line in enumerate(lines[:3]):
            if line.startswith('#!') or re.match(r"^\s*['\"]use strict['\"]\s*;?\s*$", line):
                insert_at = i + 1
        lines.insert(insert_at, "'use client'\n\n")
        path.write_text(''.join(lines), encoding='utf-8')

def main():
    root = Path(__file__).parent.resolve()
    for base in INCLUDE_DIRS:
        for path in (root / base).rglob('*'):
            if path.is_file() and path.suffix in EXTENSIONS:
                process_file(path)
    print("✔ Traitement terminé.")

if __name__ == '__main__':
    main()
