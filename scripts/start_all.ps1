# Launch both Backend and Frontend in separate PowerShell processes
$projectRoot = "$PSScriptRoot\.."

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Intelligent Career Path Planning Agent Launcher " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "$projectRoot\scripts\start_backend.ps1"

# Wait 2 seconds for backend to initialize
Start-Sleep -Seconds 2

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "$projectRoot\scripts\start_frontend.ps1"

Write-Host "Backend running on: http://127.0.0.1:8000 (Swagger docs at /docs)" -ForegroundColor Yellow
Write-Host "Frontend running on: http://localhost:5173" -ForegroundColor Yellow
