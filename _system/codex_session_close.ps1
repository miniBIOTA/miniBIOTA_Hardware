param(
    [switch]$StageAll,
    [string]$CommitMessage,
    [switch]$Push
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot

Set-Location $repoRoot

Write-Host "== miniBIOTA Hardware Codex Session Close =="
Write-Host "Repo: $repoRoot"
Write-Host ""

Write-Host "[1/3] Git status"
git status --short
Write-Host ""

Write-Host "[2/3] Reminder"
Write-Host "If hardware state, priorities, milestones, risks, or cross-domain dependencies changed,"
Write-Host "update M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md."
Write-Host "If docs changed, sync Brain mirrored docs before final closeout."
Write-Host ""

Write-Host "[3/3] Git actions"
if ($StageAll) {
    Write-Host "Running: git add ."
    git add .
    Write-Host ""
} else {
    Write-Host "Skipping git add. Pass -StageAll to stage changes."
}

if ($CommitMessage) {
    Write-Host "Running: git commit -m `"$CommitMessage`""
    git commit -m $CommitMessage
    Write-Host ""
} else {
    Write-Host "Skipping commit. Pass -CommitMessage to create a commit."
}

if ($Push) {
    if (-not $CommitMessage) {
        throw "Cannot push without a commit in this helper. Pass -CommitMessage and usually -StageAll."
    }
    Write-Host "Running: git push"
    git push
} else {
    Write-Host "Skipping push. Pass -Push to push the current branch."
}
