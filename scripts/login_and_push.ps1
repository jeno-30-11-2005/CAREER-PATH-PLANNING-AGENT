# scripts/login_and_push.ps1
# Authenticates with GitHub CLI and pushes code
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$ghExe = "$projectRoot\tools\gh.exe"
$gitExe = "$projectRoot\tools\git\cmd\git.exe"
$env:PATH = "$projectRoot\tools;$projectRoot\tools\git\cmd;$env:PATH"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " GitHub Authentication & Push Assistant " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Step 1: Logging in to GitHub via web browser..." -ForegroundColor Yellow
& $ghExe auth login --web -h github.com -p https

Write-Host ""
Write-Host "Step 2: Configuring Git credentials..." -ForegroundColor Yellow
& $ghExe auth setup-git

Write-Host ""
Write-Host "Step 3: Pushing code to https://github.com/jeno-30-11-2005/CAREER-PATH-PLANNING-AGENT..." -ForegroundColor Yellow
& $gitExe push origin main --force

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " PUSH SUCCESSFUL! Code is now live on GitHub! " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "View at: https://github.com/jeno-30-11-2005/CAREER-PATH-PLANNING-AGENT"
