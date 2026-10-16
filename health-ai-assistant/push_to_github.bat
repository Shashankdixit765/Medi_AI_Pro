@echo off
title Push MediAI Pro to GitHub
color 0a
echo =========================================================================
echo             Push MediAI Pro to your GitHub Account
echo                  Created by Shashank Dixit
echo =========================================================================
echo.
set /p REPO_URL="Enter your GitHub Repository URL (e.g. https://github.com/username/repo-name.git): "

if "%REPO_URL%"=="" (
    echo [!] No URL entered. Exiting...
    pause
    exit /b
)

echo.
echo [*] Adding git remote origin...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [*] Pushing to GitHub (branch: main)...
git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo [SUCCESS] Your project has been uploaded to GitHub successfully!
) else (
    echo [!] Push failed or authentication needed. Please check your credentials and repo permissions.
)
echo.
pause
