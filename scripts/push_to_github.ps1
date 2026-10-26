# Push to GitHub helper script
param (
    [string]$RepoUrl
)

$gitExe = "$PSScriptRoot\..\tools\git\cmd\git.exe"

if (-not $RepoUrl) {
    $RepoUrl = Read-Host "Please enter your GitHub repository URL (e.g. https://github.com/your-username/career-path-agent.git)"
}

if (-not $RepoUrl) {
    Write-Host "Error: Repository URL cannot be empty." -ForegroundColor Red
    exit 1
}

Write-Host "Configuring remote origin: $RepoUrl" -ForegroundColor Cyan
& $gitExe remote remove origin 2>$null
& $gitExe remote add origin $RepoUrl

Write-Host "Pushing main branch to GitHub..." -ForegroundColor Cyan
& $gitExe push -u origin main

Write-Host "Push completed successfully!" -ForegroundColor Green
