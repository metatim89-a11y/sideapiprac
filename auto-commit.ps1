# Auto-commit script using file system watcher
# Only commits when files actually change (event-driven, not polling)

$repoPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoPath

Write-Host "Starting auto-commit watcher for: $repoPath"
Write-Host "Monitoring file changes (event-driven, minimal CPU usage)..."
Write-Host "Press Ctrl+C to stop."
Write-Host ""

# Create file system watcher
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.Path = $repoPath
$watcher.Filter = "*.*"
$watcher.IncludeSubdirectories = $true
$watcher.NotifyFilter = [System.IO.NotifyFilters]::LastWrite, [System.IO.NotifyFilters]::FileName, [System.IO.NotifyFilters]::DirectoryName

# Debounce flag to prevent multiple commits in quick succession
$debounceTimer = $null
$debounceSeconds = 3  # Wait 3 seconds after last change before committing

$action = {
    param($source, $eventArgs)
    
    # Ignore .git directory changes
    if ($eventArgs.FullPath -like "*\.git*") {
        return
    }
    
    # Cancel existing timer if it exists
    if ($debounceTimer) {
        $debounceTimer.Stop()
        $debounceTimer.Dispose()
    }
    
    # Create a new debounce timer
    $script:debounceTimer = New-Object System.Timers.Timer
    $debounceTimer.Interval = $debounceSeconds * 1000
    $debounceTimer.AutoReset = $false
    
    $timerAction = {
        try {
            # Check if there are actual uncommitted changes
            $status = git status --porcelain 2>$null
            
            if ($status) {
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Changes detected, committing..."
                
                # Stage all changes
                git add -A
                
                # Create a commit with timestamp
                $timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
                $commitMessage = "Auto-commit: $timestamp"
                
                git commit -m $commitMessage -q
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ✓ Committed"
                
                # Push to remote
                git push -q 2>$null
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ✓ Pushed to GitHub"
            }
        }
        catch {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Error: $_"
        }
    }
    
    Register-ObjectEvent -InputObject $debounceTimer -EventName Elapsed -Action $timerAction -SourceIdentifier "CommitTimer" -Force | Out-Null
    $debounceTimer.Start()
}

# Register file system watcher events
Register-ObjectEvent -InputObject $watcher -EventName "Created" -Action $action -SourceIdentifier "FileCreated" | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action $action -SourceIdentifier "FileChanged" | Out-Null
Register-ObjectEvent -InputObject $watcher -EventName "Deleted" -Action $action -SourceIdentifier "FileDeleted" | Out-Null

# Keep the script running
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    $watcher.EnableRaisingEvents = $false
    $watcher.Dispose()
    Get-EventSubscriber | Unregister-Event -Force
}
