param(
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

Write-Host 'Checking Git LFS installation...'
if (-not (Get-Command git-lfs -ErrorAction SilentlyContinue)) {
    Write-Host 'Git LFS is not installed. Install it using:'
    Write-Host '  winget install --id Git.GitLFS'
    Write-Host 'Then run this script again.'
    exit 1
}

git lfs version

Write-Host 'Installing Git LFS hooks for this repository...'
if ($Force) {
    git lfs install --local --force
} else {
    git lfs install --local
}

Write-Host '`nGit LFS tracked patterns:'
git lfs track

if (Test-Path .gitignore) {
    Write-Host '`n.gitignore contents:'
    Get-Content .gitignore | Select-Object -First 40
}

if (Test-Path .gitattributes) {
    Write-Host '`n.gitattributes contents:'
    Get-Content .gitattributes
} else {
    Write-Host '`nNo .gitattributes file found. Create one to track model artifacts.'
}

Write-Host '`nGit LFS setup complete.'
Write-Host 'Add large artifact files with git add, commit, and push as usual.'
