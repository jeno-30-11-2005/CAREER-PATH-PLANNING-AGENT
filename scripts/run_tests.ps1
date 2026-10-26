# Execute Backend Pytest Suite
Set-Location "$PSScriptRoot\.."
Write-Host "Running Backend Automated Pytest Suite..." -ForegroundColor Cyan
& ".\venv\Scripts\python.exe" -m pytest backend\tests\test_career_agent.py -v
