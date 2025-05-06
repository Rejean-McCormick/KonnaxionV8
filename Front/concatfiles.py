#!/usr/bin/env python3
# concat_files.py

import os

# Liste des fichiers à concaténer (chemins relatifs à la racine du projet)
files = [
    'services/deliberate.ts',
    'services/decide.ts',
    'routes/routesEthikos.tsx',
    'pages/_app.tsx',
    'pages/_document.tsx',
    'app/layout.tsx',
    'app/page.tsx',
    'pages/ethikos/deliberate/elite.tsx',
    'pages/ethikos/deliberate/guidelines.tsx',
    'pages/ethikos/deliberate/[topic].tsx',
    'pages/ethikos/decide/elite.tsx',
    'pages/ethikos/decide/public.tsx',
    'pages/ethikos/decide/results.tsx',
    'pages/ethikos/decide/methodology.tsx',
]

output_path = 'combined.txt'

def main():
    # Ouvre (ou crée) le fichier de sortie en écriture (écrase l'existant)
    with open(output_path, 'w', encoding='utf-8') as out:
        for filepath in files:
            if os.path.exists(filepath):
                # Section pour chaque fichier existant
                out.write(f'# ===== Début de {filepath} =====\n')
                with open(filepath, 'r', encoding='utf-8') as f:
                    out.write(f.read())
                out.write(f'\n# ===== Fin de {filepath} =====\n\n')
            else:
                # Note l'absence dans le fichier de sortie
                warning = f'# ⚠️ Fichier manquant : {filepath}\n\n'
                out.write(warning)
                # Alerte dans la console
                print(f'⚠️ Fichier manquant : {filepath}')

    print(f'✅ Concaténation terminée dans "{output_path}"')

if __name__ == '__main__':
    main()
