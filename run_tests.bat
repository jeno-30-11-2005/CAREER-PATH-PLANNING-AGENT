@echo off
cd /d "%~dp0"
echo ======================================================================
echo Running Automated Verification Suite for Career Intelligence...
echo ======================================================================
.\venv\Scripts\python.exe test_system.py
pause
