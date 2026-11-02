@echo off
cd /d "%~dp0"
echo ======================================================================
echo Pushing Career Guide to GitHub...
echo Repository: https://github.com/jeno-30-11-2005/CAREER-PATH-PLANNING-AGENT.git
echo Branch: main
echo ======================================================================
git push origin main
if %errorlevel% equ 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] Successfully pushed all commits to GitHub!
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo [ERROR] Git push failed.
    echo If GitHub asks for a password, please use your Personal Access Token (PAT).
    echo ======================================================================
)
pause
