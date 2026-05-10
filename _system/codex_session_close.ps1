$ErrorActionPreference = "Continue"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot
$companyRoot = "M:\miniBIOTA\miniBIOTA_Company"
$companyOverview = Join-Path $companyRoot "domains\hardware\hardware_overview.md"
$companyBrief = Join-Path $companyRoot "domains\hardware\hardware_brief.md"

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "== miniBIOTA Hardware Codex Session Close =="
Write-Host "Repo:   $repoRoot"
Write-Host "Report: $companyBrief"
Write-Host ""

Set-Location $repoRoot
Write-Host "Git status:"
if (Test-Path (Join-Path $repoRoot ".git")) {
    git status --short --branch
} else {
    Write-Host "Git repository not initialized in this folder."
}
Write-Host ""

Write-Host "Closeout reminders:"
Write-Host "- Promote durable rules, decisions, corrections, and recurring hazards into local memory/playbooks."
Write-Host "- Update or flag Company reporting when manager-facing Hardware state changed: $companyBrief"
Write-Host "- Keep detailed implementation context in this repo's memory, skills, references, code, and structured records."
Write-Host "- Brain is historical/archive lookup only unless a transition plan explicitly asks for it."
Write-Host "- Do not run live-control paths, firmware deployment, telemetry writes, setpoint changes, or hardware-affecting commands without explicit approval."
Write-Host "- Run the smallest meaningful verification and report changed files."
