# Install editable packages for local development (run from repo root: .\scripts\install-local.ps1)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "Installing ams-common..."
python -m pip install -e "$Root\packages\ams-common"

$services = @(
    "services\gateway",
    "services\agent-service",
    "services\orchestration-service",
    "services\tool-service",
    "services\execution-service"
)
foreach ($dir in $services) {
    Write-Host "Installing $dir (dev extras)..."
    Push-Location (Join-Path $Root $dir)
    try {
        python -m pip install -e ".[dev]"
    } finally {
        Pop-Location
    }
}

Write-Host "Done. Run stack: docker compose up --build"
