@echo off
cd /d "%~dp0"
echo ======================================================================
echo Starting Career Guide Platform...
echo Open your browser at: http://localhost:8501
echo ======================================================================
.\venv\Scripts\python.exe -m streamlit run app.py --server.port 8501
pause
