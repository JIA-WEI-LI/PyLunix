# 設定編碼為 UTF8 以避免亂碼
$OutputEncoding = [System.Text.Encoding]::UTF8

# 取得腳本所在的目錄 (即 docs 資料夾)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# 計算 .venv 的絕對路徑 (假設 .venv 在 docs 的上一層)
$PYTHON = Join-Path $ScriptDir "..\\.venv\\Scripts\\python.exe"

# 檢查 Python 是否存在
if (-not (Test-Path $PYTHON)) {
    Write-Host "找不到虛擬環境中的 Python: $PYTHON" -ForegroundColor Red
    exit 1
}

# 切換到 docs 目錄確保執行路徑正確
Set-Location $ScriptDir

# 2. 清理舊的編譯檔案
if (Test-Path "build") { 
    Write-Host "Cleaning old build directory..." -ForegroundColor Cyan
    Remove-Item -Recurse -Force "build" 
}

# 3. 編譯英文版
Write-Host "Building English version..." -ForegroundColor Green
& $PYTHON -m sphinx -b html source build/en

# 4. 編譯中文版
Write-Host "Building Traditional Chinese version..." -ForegroundColor Green
& $PYTHON -m sphinx_intl build
& $PYTHON -m sphinx -b html source build/zh_TW -D language='zh_TW'

Write-Host "Done! Docs are in docs/build/en and docs/build/zh_TW" -ForegroundColor Cyan