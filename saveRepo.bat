@echo off
REM --------------------------------------------------
REM save.bat — add, commit (avec message), push (avec upstream)
REM --------------------------------------------------

:: 1) Demander le message de commit
set /p COMMIT_MSG=Entrez le message de commit : 

:: 2) Ajouter tous les changements
git add -A

:: 3) Commit
git commit -m "%COMMIT_MSG%"

:: 4) Récupérer la branche courante
for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set "BRANCH=%%b"

:: 5) Pousser, et définir upstream si nécessaire
git push -u origin %BRANCH%

pause
