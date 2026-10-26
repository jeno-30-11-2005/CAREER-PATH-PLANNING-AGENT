@echo off
cd /d "%~dp0"
echo Starting Intelligent Career Path Planning System...
.\venv\Scripts\python.exe -m streamlit run app.py
pause
