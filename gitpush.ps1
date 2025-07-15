@echo off
cd /d %~dp0

REM Ask for commit message
set /p msg=Enter commit message: 

REM Init repo if not already
IF NOT EXIST .git (
    echo Initializing Git repo...
    git init
)

REM Add remote if not already set
git remote -v | findstr /C:"origin" >nul
IF ERRORLEVEL 1 (
    git remote add origin https://github.com/Emre-Sekeroglu/winsy
)

REM Add all files and commit
git add .
git commit -m "%msg%"

REM Rename branch to main
git branch -M main

REM Ensure correct remote URL and force push
git remote set-url origin https://github.com/Emre-Sekeroglu/winsy
git push origin main --force

echo.
echo ✅ Forced push complete!
pause
