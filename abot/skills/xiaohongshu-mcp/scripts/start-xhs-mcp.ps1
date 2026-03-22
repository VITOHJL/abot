param(
    [string]$ExePath = "",
    [int]$Port = 18060
)

$ErrorActionPreference = "Stop"

function Test-PortOpen {
    param(
        [string]$Host = "127.0.0.1",
        [int]$Port = 18060
    )
    $tcp = New-Object System.Net.Sockets.TcpClient
    try {
        $iar = $tcp.BeginConnect($Host, $Port, $null, $null)
        if (-not $iar.AsyncWaitHandle.WaitOne(800)) {
            return $false
        }
        $tcp.EndConnect($iar) | Out-Null
        return $true
    } catch {
        return $false
    } finally {
        $tcp.Close()
    }
}

if (Test-PortOpen -Port $Port) {
    Write-Output "already-running:127.0.0.1:$Port"
    exit 0
}

$candidates = @()

if ($env:ABOT_XHS_MCP_EXE) {
    $candidates += $env:ABOT_XHS_MCP_EXE
}
if ($ExePath) {
    $candidates += $ExePath
}

$candidates += "D:\deskbot\xiaohongshu-mcp-bin\xiaohongshu-mcp-windows-amd64.exe"
$candidates += (Join-Path $HOME "xiaohongshu-mcp-bin\xiaohongshu-mcp-windows-amd64.exe")

$target = $null
foreach ($path in $candidates) {
    if ($path -and (Test-Path $path)) {
        $target = (Resolve-Path $path).Path
        break
    }
}

if (-not $target) {
    Write-Output "error:executable-not-found"
    Write-Output "hint:set ABOT_XHS_MCP_EXE to your xiaohongshu-mcp executable path"
    exit 1
}

$workDir = Split-Path -Parent $target
Start-Process -FilePath $target -WorkingDirectory $workDir -WindowStyle Hidden | Out-Null

for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-PortOpen -Port $Port) {
        Write-Output "started:$target"
        Write-Output "endpoint:http://127.0.0.1:$Port/mcp"
        exit 0
    }
}

Write-Output "error:startup-timeout"
Write-Output "hint:process started but port $Port is still closed"
exit 2
