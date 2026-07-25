# 在临时副本中执行真实 PowerPoint 打开、保存和重新打开测试。
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$ReportPath,

    [string]$TempDirectory,

    [switch]$KeepWorkCopy
)

$ErrorActionPreference = 'Stop'

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)
    return (Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Release-ComObject {
    param([object]$ComObject)
    if ($null -ne $ComObject) {
        try {
            [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($ComObject)
        }
        catch {
            # 释放失败不覆盖主要测试结果。
        }
    }
}

$resolvedInput = $null
$workRoot = $null
$workCopy = $null
$app = $null
$presentation = $null
$reopened = $null
$createdApplication = $false
$createdTemporaryDirectory = $false
$result = [ordered]@{
    tool = 'test_powerpoint_roundtrip'
    input_path = $null
    input_sha256_before = $null
    input_sha256_after = $null
    work_copy = $null
    work_copy_retained = $null
    status = 'SCRIPT_ERROR'
    message = $null
    started_utc = [DateTime]::UtcNow.ToString('o')
    finished_utc = $null
}

try {
    $resolvedInput = (Resolve-Path -LiteralPath $InputPath).Path
    $result.input_path = $resolvedInput
    $result.input_sha256_before = Get-Sha256 -LiteralPath $resolvedInput

    if ([IO.Path]::GetExtension($resolvedInput) -ne '.pptx') {
        throw '输入文件扩展名不是 .pptx。'
    }

    $existing = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue)
    if ($existing.Count -gt 0) {
        $result.status = 'SKIPPED_EXISTING_POWERPOINT'
        $result.message = '检测到用户已有 PowerPoint 进程。为避免关闭或干扰用户实例，脚本拒绝自动测试。'
        $result.input_sha256_after = Get-Sha256 -LiteralPath $resolvedInput
        $result.finished_utc = [DateTime]::UtcNow.ToString('o')
        $reportFullPath = [IO.Path]::GetFullPath($ReportPath)
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($reportFullPath)) | Out-Null
        $result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportFullPath -Encoding UTF8
        Write-Warning $result.message
        exit 3
    }

    if ([string]::IsNullOrWhiteSpace($TempDirectory)) {
        $workRoot = Join-Path ([IO.Path]::GetTempPath()) ('ppt-roundtrip-' + [Guid]::NewGuid().ToString('N'))
        $createdTemporaryDirectory = $true
    }
    else {
        $workRoot = [IO.Path]::GetFullPath($TempDirectory)
    }
    [IO.Directory]::CreateDirectory($workRoot) | Out-Null
    $workCopy = Join-Path $workRoot ([IO.Path]::GetFileName($resolvedInput))
    Copy-Item -LiteralPath $resolvedInput -Destination $workCopy -Force
    $result.work_copy = $workCopy
    $result.work_copy_retained = $true

    $app = New-Object -ComObject PowerPoint.Application
    $createdApplication = $true

    # Open(FileName, ReadOnly, Untitled, WithWindow)
    $presentation = $app.Presentations.Open($workCopy, $false, $false, $false)
    $presentation.Save()
    $presentation.Close()
    Release-ComObject -ComObject $presentation
    $presentation = $null

    $reopened = $app.Presentations.Open($workCopy, $true, $false, $false)
    $slideCount = $reopened.Slides.Count
    $reopened.Close()
    Release-ComObject -ComObject $reopened
    $reopened = $null

    $result.status = 'PASS'
    $result.message = "临时副本已完成打开、保存和重新打开；幻灯片数量：$slideCount。"
}
catch {
    if ($result.status -eq 'SCRIPT_ERROR') {
        $result.status = 'FAIL'
    }
    $result.message = $_.Exception.Message
}
finally {
    if ($null -ne $reopened) {
        try { $reopened.Close() } catch {}
        Release-ComObject -ComObject $reopened
    }
    if ($null -ne $presentation) {
        try { $presentation.Close() } catch {}
        Release-ComObject -ComObject $presentation
    }
    if ($createdApplication -and $null -ne $app) {
        try { $app.Quit() } catch {}
        Release-ComObject -ComObject $app
    }

    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()

    if ($null -ne $resolvedInput -and (Test-Path -LiteralPath $resolvedInput)) {
        $result.input_sha256_after = Get-Sha256 -LiteralPath $resolvedInput
    }

    if (
        $result.status -eq 'PASS' -and
        $createdTemporaryDirectory -and
        -not $KeepWorkCopy -and
        $null -ne $workRoot -and
        (Test-Path -LiteralPath $workRoot)
    ) {
        try {
            $resolvedWorkRoot = (Resolve-Path -LiteralPath $workRoot).Path
            $resolvedSystemTemp = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\')
            if ($resolvedWorkRoot.StartsWith($resolvedSystemTemp + '\ppt-roundtrip-', [StringComparison]::OrdinalIgnoreCase)) {
                Remove-Item -LiteralPath $resolvedWorkRoot -Recurse -Force
                $result.work_copy_retained = $false
            }
        }
        catch {
            # 清理失败不改变 PowerPoint roundtrip 主结果。
        }
    }

    $result.finished_utc = [DateTime]::UtcNow.ToString('o')

    try {
        $reportFullPath = [IO.Path]::GetFullPath($ReportPath)
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($reportFullPath)) | Out-Null
        $result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportFullPath -Encoding UTF8
    }
    catch {
        Write-Error "无法写入报告：$($_.Exception.Message)"
        exit 2
    }
}

Write-Output $result.message
if ($result.input_sha256_before -ne $result.input_sha256_after) {
    Write-Error '原始输入文件哈希发生变化。'
    exit 2
}
if ($result.status -eq 'PASS') {
    exit 0
}
exit 1
