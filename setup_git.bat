@echo off
REM Git setup script for GameStoryTeller (Windows)

echo 🚀 Setting up Git repository for GameStoryTeller...

REM Initialize git if not already done
if not exist ".git" (
    git init
    echo ✅ Git initialized
) else (
    echo ✅ Git already initialized
)

REM Add remote (will fail if already exists, that's okay)
git remote add origin https://github.com/DARKxGHOST11/GameStoryTeller.git 2>nul || git remote set-url origin https://github.com/DARKxGHOST11/GameStoryTeller.git

echo ✅ Remote repository configured

REM Add all files
git add .

echo ✅ Files staged

REM Commit
git commit -m "Initial commit: Epic Game Story Generator with Galaxy UI - Production ready for Vercel"

echo ✅ Changes committed

echo.
echo 📤 Ready to push! Run:
echo    git push -u origin main
echo.
echo Or if your default branch is 'master':
echo    git push -u origin master
echo.

pause

