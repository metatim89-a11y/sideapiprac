@echo off
REM Auto-commit watcher starter for Windows
REM This script runs the PowerShell auto-commit script in the background

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "scriptDir=%~dp0"

REM Check if PowerShell is available
where powershell >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: PowerShell is not installed or not in PATH
    pause
    exit /b 1
)

REM Run the PowerShell script in a new window (keeps it visible)
echo Starting auto-commit watcher...
echo Files will be automatically committed every 30 seconds
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%scriptDir%auto-commit.ps1"
