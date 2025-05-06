#!/usr/bin/env python3
# rename_list.py  – Renomme une liste fixe de fichiers .js → .tsx
# NOTE : lance ce script depuis la racine du projet “next-enterprise”

from pathlib import Path
from shutil import move

# --- liste (relative au dossier courant) ------------------------------
FILES = [
    "pages/_document.js",
    # ---------- components/user-components ----------
    "components/user-components/UserVisit.js",
    "components/user-components/UserProfile.js",
    "components/user-components/UserLikes.js",
    "components/user-components/UserComments.js",
    "components/user-components/style.js",
    "components/user-components/index.js",
    # ---------- components/shared ----------
    "components/shared/utils.js",
    # ---------- sculpture‑maker ----------
    "components/sculpture-maker-components/style.js",
    "components/sculpture-maker-components/SculptureGrid.js",
    "components/sculpture-maker-components/MakerList.js",
    "components/sculpture-maker-components/SculptureDetail/SculptureTrend.js",
    "components/sculpture-maker-components/SculptureDetail/SculptureComment.js",
    "components/sculpture-maker-components/SculptureDetail/index.js",
    "components/sculpture-maker-components/EditForm/SculptureEdit.js",
    "components/sculpture-maker-components/EditForm/MakerEdit.js",
    "components/sculpture-maker-components/EditForm/index.js",
    "components/sculpture-maker-components/EditForm/EditImage.js",
    "components/sculpture-maker-components/EditForm/EditFormTextFields.js",
    "components/sculpture-maker-components/CreateForm/SculptureUploadImage.js",
    "components/sculpture-maker-components/CreateForm/SculptureCreate.js",
    "components/sculpture-maker-components/CreateForm/MakerCreate.js",
    "components/sculpture-maker-components/CreateForm/index.js",
    "components/sculpture-maker-components/CreateForm/CreateFormTextFields.js",
    # ---------- map ----------
    "components/map-components/StaticMap.js",
    "components/map-components/MapMarker.js",
    "components/map-components/Map.js",
    "components/map-components/index.js",
    "components/map-components/ControlPanel.js",
    # ---------- layout ----------
    "components/layout-components/Sider.js",
    "components/layout-components/Main.js",
    "components/layout-components/LogoTitle.js",
    "components/layout-components/Drawer.js",
    # ---------- dashboard ----------
    "components/dashboard-components/VisitCard.js",
    "components/dashboard-components/UserPieChart.js",
    "components/dashboard-components/UserCard.js",
    "components/dashboard-components/style.js",
    "components/dashboard-components/SculptureTable.js",
    "components/dashboard-components/LikeCard.js",
    "components/dashboard-components/index.js",
    "components/dashboard-components/CommentCard.js",
    # ---------- auth0 ----------
    "components/auth0-components/index.js",
    # ---------- activity ----------
    "components/activity-components/style.js",
    "components/activity-components/RecentVisits.js",
    "components/activity-components/RecentLikes.js",
    "components/activity-components/RecentComments.js",
    "components/activity-components/index.js",
]

# ----------------------------------------------------------------------
root = Path.cwd()
renamed, missing = [], []

for rel in FILES:
    src = root / rel
    if not src.exists():
        missing.append(rel)
        continue
    dst = src.with_suffix(".tsx")
    move(src, dst)
    renamed.append((src, dst))

# --- résumé -----------------------------------------------------------
print(f"\n✅  {len(renamed)} fichier(s) renommé(s) :")
for s, d in renamed:
    print(f"   {s.relative_to(root)} → {d.relative_to(root)}")

if missing:
    print("\n⚠️  Ces fichiers n’ont pas été trouvés :")
    for m in missing:
        print(f"   {m}")

print("\n💡  Pense à lancer un `pnpm lint --fix` ou équivalent pour corriger les imports cassés.")
