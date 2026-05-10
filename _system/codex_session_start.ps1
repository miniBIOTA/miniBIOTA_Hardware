$ErrorActionPreference = "Continue"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot
$companyRoot = "M:\miniBIOTA\miniBIOTA_Company"
$companyRegistry = Join-Path $companyRoot "_system\agent_repo_registry.md"
$companyOverview = Join-Path $companyRoot "domains\hardware\hardware_overview.md"
$companyBrief = Join-Path $companyRoot "domains\hardware\hardware_brief.md"

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

Write-Host "== miniBIOTA Hardware Codex Session Start =="
Write-Host "Repo:    $repoRoot"
Write-Host "Company: $companyRoot"
Write-Host "Report:  $companyBrief"
Write-Host ""

Write-Host "[1/3] Write policy"
if ($env:MINIBIOTA_WRITE_MODE) {
    Write-Host "MINIBIOTA_WRITE_MODE: $env:MINIBIOTA_WRITE_MODE"
} else {
    Write-Host "MINIBIOTA_WRITE_MODE is not set. Follow AGENTS.md and ask before high-impact writes."
}
Write-Host "Do not run live-control paths, firmware deployment, telemetry writes, setpoint changes, or hardware-affecting commands without explicit approval."
Write-Host ""

Write-Host "[2/3] Git status"
Set-Location $repoRoot
if (Test-Path (Join-Path $repoRoot ".git")) {
    git status --short --branch
} else {
    Write-Host "Git repository not initialized in this folder."
}
Write-Host ""

Write-Host "[3/3] Read these files first:"
Write-Host "- AGENTS.md"
Write-Host "- memory/00-index.md"
Write-Host "- relevant memory files and skills/*/SKILL.md playbooks"
Write-Host "- Company registry when routing or reporting matters: $companyRegistry"
Write-Host "- Company report when manager-facing state matters: $companyBrief"
Write-Host "- Company overview when broad domain context matters: $companyOverview"
Write-Host "- Brain only for historical, archive, transition, or recovery lookup"
Write-Host ""
Write-Host "Startup complete. Normal routing and reporting now go through Company/domain sources, not Brain."
