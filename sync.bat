@echo off
setlocal
<<<<<<< HEAD
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
endlocal
=======
REM ============================================================================
REM sync.bat - Zero-Friction Execution Wrapper for sync.ps1
REM Automatically bypasses PowerShell ExecutionPolicy across fresh clones/devices.
REM ============================================================================

where pwsh >nul 2>nul
if %ERRORLEVEL% equ 0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
)
exit /b %ERRORLEVEL%
>>>>>>> 9deb2a5 (feat(curriculum): integrate three-layer first-principles framework and sync.bat companion)
