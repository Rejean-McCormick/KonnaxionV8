@echo off
REM --------------------------------------------
REM save.bat — add, commit (avec message), push
REM --------------------------------------------

:: Demande du message de commit
set /p COMMIT_MSG=Entrez le message de commit : 

:: Ajout de tous les changements
git add -A

:: Commit avec le message saisi
git commit -m "%COMMIT_MSG%"

:: Push sur la branche courante
git push

pause
