# scripts/dev.ps1
# 启动本地 Jekyll 开发服务器，前置自动清理。
#
# 解决的问题：
#   1. _config.yml 改动后 Jekyll --watch 不会重读，必须重启进程
#   2. Windows 下旧 Jekyll 进程可能不被正确终止（孤儿 ruby.exe 仍占 4000 端口）
#      → 出现"多进程抢端口、HTTP 请求随机命中、站点标题来回变"
#
# 用法（在仓库根目录）：
#   pwsh -File scripts/dev.ps1
#   或：.\scripts\dev.ps1
#
# 参数：
#   -Clean  额外删除 _site / .jekyll-cache，强制全量重建
#   -Port   指定端口（默认 4000）

[CmdletBinding()]
param(
    [switch]$Clean,
    [int]$Port = 4000
)

$ErrorActionPreference = 'Stop'

# ---------- 1. 扫端口、杀残留 ----------
Write-Host "[1/3] 扫描端口 $Port ..." -ForegroundColor Cyan
$conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
$procIds = @($conns | Select-Object -ExpandProperty OwningProcess -Unique)

if ($procIds.Count -gt 0) {
    foreach ($procId in $procIds) {
        $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Host "  ⛔ 杀掉 PID $procId  ($($proc.ProcessName))" -ForegroundColor Yellow
            try { Stop-Process -Id $procId -Force -ErrorAction Stop } catch {}
        }
    }
    Start-Sleep -Seconds 2
}

# 再扫一次确认端口干净
$still = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($still) {
    Write-Host "  ❌ 端口 $Port 仍被占用，请手动检查：netstat -ano | findstr :$Port" -ForegroundColor Red
    exit 1
} else {
    Write-Host "  ✅ 端口 $Port 干净" -ForegroundColor Green
}

# ---------- 2. 可选：清缓存 ----------
if ($Clean) {
    Write-Host "[2/3] 清理 _site / .jekyll-cache ..." -ForegroundColor Cyan
    foreach ($dir in @('_site', '.jekyll-cache')) {
        if (Test-Path $dir) {
            Remove-Item -Recurse -Force $dir
            Write-Host "  🗑  已删除 $dir" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "[2/3] 跳过清缓存（加 -Clean 强制清理）" -ForegroundColor DarkGray
}

# ---------- 3. 启动 Jekyll ----------
Write-Host "[3/3] 启动 Jekyll （http://127.0.0.1:$Port/  ·  livereload）..." -ForegroundColor Cyan
Write-Host "      Ctrl+C 退出" -ForegroundColor DarkGray
Write-Host ""

bundle exec jekyll serve --livereload --port $Port
