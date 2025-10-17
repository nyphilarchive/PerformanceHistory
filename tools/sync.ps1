Param(
  [string]$Solr = $env:SOLR_URL
)

# Load .env if present for local overrides
if (Test-Path .env) {
  Get-Content .env | ForEach-Object {
    if (-not [string]::IsNullOrWhiteSpace($_) -and -not $_.Trim().StartsWith('#')) {
      $kv = $_.Split('=',2)
      if ($kv.Count -eq 2) { $env:$($kv[0].Trim()) = $kv[1].Trim() }
    }
  }
  if (-not $Solr -or $Solr -eq "") { $Solr = $env:SOLR_URL }
}

if (-not $Solr -or $Solr -eq "") {
  Write-Host "SOLR_URL is not set. Define it in .env or pass -Solr." -ForegroundColor Red
  exit 1
}

Write-Host "Running full Performance History pipeline..." -ForegroundColor Cyan

# Check for requests presence; avoid installing unless necessary
$checkCmd = @'
import sys
try:
    import requests  # noqa: F401
    sys.exit(0)
except Exception:
    sys.exit(1)
'@
python -c $checkCmd
if ($LASTEXITCODE -ne 0) {
  Write-Host "Missing Python dependency: requests" -ForegroundColor Yellow
  Write-Host "Create a virtualenv and install requirements, e.g.:" -ForegroundColor Yellow
  Write-Host "  python -m venv .venv; . .venv\\Scripts\\Activate.ps1; pip install -r requirements.txt" -ForegroundColor Yellow
  exit 1
}

python tools/pipeline.py all --solr $Solr
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Done." -ForegroundColor Green
