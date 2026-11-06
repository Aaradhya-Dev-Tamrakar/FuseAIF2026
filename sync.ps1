<#
.SYNOPSIS
Synchronize the current branch with origin and stop on Git failures.
.EXAMPLE
.\sync.bat -m "docs: update archive" -Paths docs/chat_history
#>
[CmdletBinding(SupportsShouldProcess)]
param([Alias('m')][string]$Message, [switch]$PullOnly, [string[]]$Paths)
$ErrorActionPreference = 'Stop'
function Invoke-Git {
 param([Parameter(ValueFromRemainingArguments)][string[]]$GitArgs)
 $result = & git @GitArgs
 if ($LASTEXITCODE -ne 0) { throw "git $($GitArgs -join ' ') failed (exit $LASTEXITCODE)." }
 return $result
}
try {
 Set-Location $PSScriptRoot
 $branch = Invoke-Git symbolic-ref --quiet --short HEAD
 if (-not $branch) { throw 'A named branch is required.' }
 if ($WhatIfPreference) {
  Write-Host "Preview: synchronize origin/$branch; paths: $($Paths -join ', ')"
  Invoke-Git status --short
  exit 0
 }
 Invoke-Git fetch origin
 & git show-ref --verify --quiet "refs/remotes/origin/$branch"
 $remoteStatus = $LASTEXITCODE
 if ($remoteStatus -eq 0) { Invoke-Git merge --ff-only "origin/$branch" }
 elseif ($remoteStatus -ne 1) { throw 'Unable to inspect the remote branch.' }
 elseif ($PullOnly) { throw "No remote branch origin/$branch exists." }
 if ($PullOnly) { exit 0 }
 if ($Paths) {
  $alreadyStaged = @(Invoke-Git diff --cached --name-only)
  if ($alreadyStaged.Count) { throw 'Scoped sync requires an empty index.' }
  Invoke-Git add -- @Paths
 } else { Invoke-Git add --all }
 $staged = @(Invoke-Git diff --cached --name-only)
 if ($staged.Count) {
  Invoke-Git diff --cached --check
  if (-not $Message) { $Message = 'chore: synchronize repository changes' }
  Invoke-Git commit -m $Message
 }
 Invoke-Git push --set-upstream origin "HEAD:refs/heads/$branch"
 Write-Host "Synchronized origin/$branch."
} catch {
 Write-Error $_ -ErrorAction Continue
 exit 1
}
