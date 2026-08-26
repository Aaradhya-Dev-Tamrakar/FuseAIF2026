<#
.SYNOPSIS
    Automates Git pull, auto-commit message generation, and push for this repo.

.DESCRIPTION
    Curated for fuseAiF_wk12_ner_customer_support (no commit-back bot, no search-index
    extractor, no tracker file — unlike the portfolio repo's sync.ps1, none of those
    exist here), so this version just:
    1. Pulls with --autostash so your local work is preserved.
    2. Auto-generates a conventional commit message if none is provided.
    3. Stages, commits, and pushes (retries once via rebase if push is rejected).

.EXAMPLE
    .\sync.ps1                               # Auto commit message, add, commit & push
    .\sync.ps1 -m "custom commit message"     # Uses custom commit message
    .\sync.ps1 -PullOnly                     # Only pull without committing/pushing
#>

param (
    [Alias("m")]
    [string]$Message,

    [switch]$PullOnly
)

$ErrorActionPreference = "Continue"

function Get-AutoCommitMessage {
    $statusLines = git status --porcelain
    if (-not $statusLines) {
        return $null
    }

    $modifiedFiles = @()
    $addedFiles = @()
    $deletedFiles = @()

    foreach ($line in $statusLines) {
        $status = $line.Substring(0, 2).Trim()
        $file = $line.Substring(3).Trim()
        $fileName = Split-Path $file -Leaf

        if ($status -match 'A|\?\?') {
            $addedFiles += $fileName
        }
        elseif ($status -match 'D') {
            $deletedFiles += $fileName
        }
        else {
            $modifiedFiles += $fileName
        }
    }

    $allChanged = $addedFiles + $modifiedFiles + $deletedFiles
    if ($allChanged.Count -eq 0) {
        return $null
    }

    $prefix = "chore"
    if ($addedFiles.Count -gt 0) {
        $prefix = "feat"
    }
    elseif ($modifiedFiles | Where-Object { $_ -match '^README\.md$' -or $_ -match '\.md$' }) {
        $prefix = "docs"
    }
    elseif ($modifiedFiles | Where-Object { $_ -match '\.(ipynb|ps1)$' }) {
        $prefix = "refactor"
    }

    $summary = ""
    if ($allChanged.Count -le 3) {
        $summary = $allChanged -join ", "
    }
    else {
        $firstTwo = ($allChanged[0..1]) -join ", "
        $extraCount = $allChanged.Count - 2
        $summary = "$firstTwo +$extraCount more"
    }

    return "${prefix}: update ${summary}"
}

Write-Host "[Git Sync] Pulling latest changes from origin main..." -ForegroundColor Cyan
git pull --autostash origin main

if ($PullOnly) {
    Write-Host "[Git Sync] Pull complete (PullOnly flag set)." -ForegroundColor Green
    exit 0
}

if (-not $Message) {
    $Message = Get-AutoCommitMessage
    if ($Message) {
        Write-Host "[Git Sync] Auto-generated commit message: '$Message'" -ForegroundColor Yellow
    }
}

if ($Message) {
    Write-Host "[Git Sync] Staging changes..." -ForegroundColor Cyan
    git add .

    Write-Host "[Git Sync] Committing: '$Message'..." -ForegroundColor Cyan
    git commit -m "$Message"

    Write-Host "[Git Sync] Pushing to origin main..." -ForegroundColor Cyan
    git push origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[Git Sync] Push rejected. Re-pulling and retrying push..." -ForegroundColor Yellow
        git pull --rebase --autostash origin main
        git push origin main
    }
}
else {
    Write-Host "[Git Sync] No local changes detected to commit." -ForegroundColor Gray
}

Write-Host "[Git Sync] Workspace is clean and fully synchronized!" -ForegroundColor Green
