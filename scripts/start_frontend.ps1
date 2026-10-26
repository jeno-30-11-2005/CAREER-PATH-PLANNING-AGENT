# Launch React Frontend
Write-Host "Starting React Frontend on http://localhost:5173..." -ForegroundColor Magenta
$nodeDir = "$PSScriptRoot\..\tools\nodejs"
$env:PATH = "$nodeDir;$env:PATH"
Set-Location "$PSScriptRoot\..\frontend"
npm run dev
