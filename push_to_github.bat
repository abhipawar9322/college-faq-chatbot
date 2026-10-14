@echo off
title Push Project to GitHub
echo ========================================================
echo       Deploy College FAQ Chatbot to GitHub
echo ========================================================
echo.

:: Check if git is installed
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not found in system PATH.
    echo Please install Git for Windows from: https://git-scm.com/
    pause
    exit /b 1
)

echo [1/5] Initializing Git repository...
if not exist ".git" (
    git init
) else (
    echo Git repository is already initialized.
)

echo.
echo [2/5] Staging project files...
git add .

echo.
echo [3/5] Creating commit...
git commit -m "feat: AI FAQ Chatbot for College and Placement Queries using NLP and Streamlit"

echo.
echo [4/5] Setting main branch...
git branch -M main

echo.
set /p REPO_URL="Enter your GitHub Repo URL (e.g. https://github.com/username/college-faq-chatbot.git): "

if "%REPO_URL%"=="" (
    echo [ERROR] No repository URL entered. Aborting push.
    pause
    exit /b 1
)

echo.
echo [5/5] Connecting to remote and pushing...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo Pushing to GitHub (a sign-in browser popup may appear)...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo  SUCCESS! Project successfully pushed to GitHub!
    echo ========================================================
) else (
    echo.
    echo [NOTICE] If the push failed, please make sure:
    echo 1. The GitHub repository is empty (no existing README or commits).
    echo 2. You have permission to push to %REPO_URL%.
    echo 3. You signed in when prompted by the Git Credential Manager.
)

echo.
pause
